# bot/utils.py

import discord
import json
import logging
from discord import Embed, Color

def get_color_and_emoji(status):
    """
    Determines the color and emoji based on the status of the event.

    Parameters:
    - status (str): The status string (e.g., "success", "failure").

    Returns:
    - tuple: (discord.Color, str) corresponding color and emoji.
    """
    status = status.lower()
    if status in ["completed", "success", "passed", "merged", "active", "commented", "approved"]:
        return Color.green(), "✅"
    elif status in ["in_progress", "queued", "waiting", "running", "started"]:
        return Color.orange(), "⏳"
    elif status in ["failure", "failed", "error", "cancelled", "declined", "changes_requested"]:
        return Color.red(), "❌"
    else:
        return Color.blurple(), "ℹ️"

def build_embed(key, data, handler_name=None):
    """
    Constructs a Discord embed based on the data associated with the unique key.

    Parameters:
    - key (str): The unique key for the "thing" (e.g., "push:abcd1234").
    - data (dict): The data associated with the key.
    - handler_name (str, optional): The name of the event handler that processed this event.

    Returns:
    - discord.Embed: The constructed Discord embed.
    """
    try:
        kind, ident = key.split(':', 1)
    except ValueError:
        kind, ident = "unknown", key

    logging.debug(f"build_embed called with kind='{kind}', ident='{ident}', handler_name='{handler_name}'")

    embed = Embed(color=Color.blurple())  # Default color

    if kind == "push":
        # Building an embed for a push event
        message = data.get("message", "(no message)")
        url = data.get("url", "#")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")
        emoji = "🔀"
        color, emoji = get_color_and_emoji("success")
        embed.color = color
        embed.title = f"{emoji} Push to {repo_full_name}"
        embed.url = url
        embed.description = f"**Commit Message:** {message}\n[View Commit]({url})"
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()
        logging.info(f"Built embed for push event: {key}")

    elif kind == "pull_request":
        # Building an embed for a pull request event
        title = data.get("title", "(no title)")
        url = data.get("url", "#")
        action = data.get("action", "unknown")
        merged = data.get("merged", False)
        repo_full_name = data.get("repo_full_name", "unknown/unknown")
        emoji = "🔀" if merged else "📄"
        color, emoji = get_color_and_emoji("merged" if merged else action)
        embed.color = color
        embed.title = f"{emoji} Pull Request: {title}"
        embed.url = url
        embed.description = f"**Action:** {action.capitalize()}\n**Repository:** {repo_full_name}\n[View PR]({url})"
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()
        logging.info(f"Built embed for pull_request event: {key}")

    elif kind == "issue_comment":
        # Building an embed for an issue comment event
        commenter = data.get("user", "unknown")
        comment_body = data.get("body", "")
        comment_url = data.get("url", "#")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")
        emoji = "💬"
        color = Color.blue()
        embed.color = color
        embed.title = f"{emoji} Issue Comment by {commenter}"
        embed.url = comment_url
        embed.description = f"**Comment:** {comment_body}\n[View Comment]({comment_url})"
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()
        logging.info(f"Built embed for issue_comment event: {key}")

    elif kind == "commit_comment":
        # Building an embed for a commit comment event
        commit_sha = data.get("commit_sha", "unknown")
        commenter = data.get("commenter", "unknown")
        comment_url = data.get("url", "#")
        body = data.get("body", "")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")
        emoji = "💬"
        color, emoji = get_color_and_emoji("commented")
        embed.color = color
        embed.title = f"{emoji} Commit Comment by {commenter}"
        embed.url = comment_url
        embed.description = (
            f"**Commit SHA:** [{commit_sha[:7]}](https://github.com/{repo_full_name}/commit/{commit_sha})\n"
            f"**Commenter:** {commenter}\n"
            f"**Comment:** {body[:80]}...\n[View Comment]({comment_url})"
        )
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()
        logging.info(f"Built embed for commit_comment event: {key}")

    elif kind == "check_run":
        # Building an embed for a check run event
        name = data.get("name", "Unnamed Check")
        url = data.get("url", "#")
        status = data.get("status", "unknown")
        conclusion = data.get("conclusion", "unknown")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")
        overall_status = conclusion if status == "completed" else status
        color, emoji = get_color_and_emoji(overall_status)
        embed.color = color
        embed.title = f"{emoji} Check Run: {name}"
        embed.url = url
        embed.description = f"**Status:** {overall_status.capitalize()}\n[View Check Run]({url})"
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()
        logging.info(f"Built embed for check_run event: {key}")

    elif kind == "check_suite":
        # Building an embed for a check suite event
        name = data.get("name", "Unnamed Check Suite")
        url = data.get("url", "#")
        status = data.get("status", "unknown")
        conclusion = data.get("conclusion", "unknown")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")
        overall_status = conclusion if status == "completed" else status
        color, emoji = get_color_and_emoji(overall_status)
        embed.color = color
        embed.title = f"{emoji} Check Suite: {name}"
        embed.url = url
        embed.description = f"**Status:** {overall_status.capitalize()}\n[View Check Suite]({url})"
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()
        logging.info(f"Built embed for check_suite event: {key}")

    elif kind == "workflow_run":
        # Building an embed for a workflow run event
        name = data.get("name", "Unnamed Workflow")
        url = data.get("url", "#")
        status = data.get("status", "unknown")
        conclusion = data.get("conclusion", "unknown")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")
        overall_status = conclusion if status == "completed" else status
        color, emoji = get_color_and_emoji(overall_status)
        embed.color = color
        embed.title = f"{emoji} Workflow Run: {name}"
        embed.url = url
        embed.description = f"**Status:** {overall_status.capitalize()}\n[View Workflow Run]({url})"
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()
        logging.info(f"Built embed for workflow_run event: {key}")

    elif kind == "workflow_job":
        # Building an embed for a workflow job event
        name = data.get("name", "Unnamed Workflow Job")
        url = data.get("url", "#")
        status = data.get("status", "unknown")
        conclusion = data.get("conclusion", "unknown")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")
        overall_status = conclusion if status == "completed" else status
        color, emoji = get_color_and_emoji(overall_status)
        embed.color = color
        embed.title = f"{emoji} Workflow Job: {name}"
        embed.url = url
        embed.description = f"**Status:** {overall_status.capitalize()}\n[View Workflow Job]({url})"
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()
        logging.info(f"Built embed for workflow_job event: {key}")

    elif kind == "create":
        # Building an embed for a create event (branch or tag creation)
        ref_type = data.get("ref_type", "unknown")
        ref = data.get("ref", "unknown")
        user = data.get("user", "unknown")
        ref_url = data.get("ref_url", "#")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")

        emoji = "➕" if ref_type == "branch" else "🏷️"
        color = Color.green() if ref_type == "branch" else Color.blue()

        embed.color = color
        embed.title = f"{emoji} {ref_type.capitalize()} Created: {ref}"
        if ref_url != "#":
            embed.url = ref_url  # Makes the title a hyperlink to the ref

        desc = f"**Type:** {ref_type.capitalize()}\n**Reference:** {ref}\n**Created By:** {user}\n[View {ref_type.capitalize()}]({ref_url})"
        embed.description = desc

        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")

        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()

        logging.info(f"Built embed for create event: {key}")

    elif kind == "delete":
        # Building an embed for a delete event (branch or tag deletion)
        ref_type = data.get("ref_type", "unknown")
        ref = data.get("ref", "unknown")
        user = data.get("user", "unknown")
        ref_url = data.get("ref_url", "#")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")

        emoji = "➖" if ref_type == "branch" else "🏷️"
        color = Color.red() if ref_type == "branch" else Color.dark_blue()

        embed.color = color
        embed.title = f"{emoji} {ref_type.capitalize()} Deleted: {ref}"
        if ref_url != "#":
            embed.url = ref_url  # Makes the title a hyperlink to the ref (if possible)

        desc = f"**Type:** {ref_type.capitalize()}\n**Reference:** {ref}\n**Deleted By:** {user}\n[View {ref_type.capitalize()}]({ref_url})"
        embed.description = desc

        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")

        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()

        logging.info(f"Built embed for delete event: {key}")

    elif kind == "fork":
        # Building an embed for a fork event
        sender = data.get("sender", "unknown")
        repo_name = data.get("repo_name", "unknown/unknown")
        forkee_name = data.get("forkee_name", "unknown")
        forkee_url = data.get("forkee_url", "#")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")

        emoji = "🍴"
        color = Color.gold()

        embed.color = color
        embed.title = f"{emoji} Repository Forked by {sender}"
        embed.url = forkee_url
        embed.description = (
            f"**Original Repository:** {repo_name}\n"
            f"**Forked Repository:** [{forkee_name}]({forkee_url})\n"
            f"[View Fork]({forkee_url})"
        )
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()

        logging.info(f"Built embed for fork event: {key}")

    elif kind == "release":
        # Building an embed for a release event
        action = data.get("action", "unknown")
        name = data.get("name", "No Name")
        url = data.get("url", "#")
        publisher = data.get("publisher", "unknown")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")

        emoji = "📦"
        color = Color.blue()

        embed.color = color
        embed.title = f"{emoji} Release {action.capitalize()}: {name}"
        embed.url = url
        embed.description = (
            f"**Name:** {name}\n"
            f"**Action:** {action.capitalize()}\n"
            f"**Publisher:** {publisher}\n"
            f"[View Release]({url})"
        )
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()

        logging.info(f"Built embed for release event: {key}")

    elif kind == "repository":
        # Building an embed for a repository event
        action = data.get("action", "unknown")
        repo_name = data.get("name", "unknown")
        repo_url = data.get("url", "#")
        owner = data.get("owner", "unknown")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")

        emoji = "🏠"
        color = Color.greyple()

        embed.color = color
        embed.title = f"{emoji} Repository {action.capitalize()}: {repo_name}"
        embed.url = repo_url
        embed.description = (
            f"**Repository:** [{repo_name}]({repo_url})\n"
            f"**Action:** {action.capitalize()}\n"
            f"**Owner:** {owner}\n"
            f"[View Repository]({repo_url})"
        )
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()

        logging.info(f"Built embed for repository event: {key}")

    elif kind == "watch":
        # Building an embed for a watch/star event
        user = data.get("user", "unknown")
        repo_name = data.get("repo_name", "unknown")
        repo_url = data.get("repo_url", "#")
        action = data.get("action", "starred")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")

        emoji = "⭐"
        color = Color.gold()

        embed.color = color
        embed.title = f"{emoji} {action.capitalize()} Repository"
        embed.url = repo_url
        embed.description = (
            f"**User:** {user}\n"
            f"**Repository:** [{repo_name}]({repo_url})\n"
            f"[View Repository]({repo_url})"
        )
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()

        logging.info(f"Built embed for watch event: {key}")

    elif kind == "member":
        # Building an embed for a member event
        member_login = data.get("member_login", "unknown")
        action = data.get("action", "unknown")
        repo_full_name = data.get("repo_full_name", "unknown/unknown")
        repo_url = data.get("repo_url", "#")

        emoji = "👥"
        color = Color.purple()

        embed.color = color
        embed.title = f"{emoji} Member {action.capitalize()}"
        embed.url = repo_url
        embed.description = (
            f"**Member:** {member_login}\n"
            f"**Action:** {action.capitalize()}\n"
            f"**Repository:** [{repo_full_name}]({repo_url})\n"
            f"[View Repository]({repo_url})"
        )
        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()

        logging.info(f"Built embed for member event: {key}")

    else:
        # Handling Unexpected Events
        embed.title = "⚙️ Other Event"
        embed.description = "No detailed storage for this event."
        embed.color = Color.greyple()
        embed.set_author(name="GitHub Watcher", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")

        if handler_name:
            embed.set_footer(text=f"Handled by: {handler_name}")

        try:
            json_payload = json.dumps(data, indent=2)
            if len(json_payload) > 1800:
                json_payload = json_payload[:1800] + "...\n```json\n[Truncated]"
            embed.add_field(name="Event Payload", value=f"```json\n{json_payload}```", inline=False)
        except Exception as e:
            embed.add_field(name="Error", value=f"Failed to serialize event payload: {e}", inline=False)

        embed.timestamp = discord.utils.utcnow()

        logging.info(f"Built embed for other event: {key}")

    return embed
