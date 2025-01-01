# handlers/github_handlers.py

import asyncio
import logging

class GitHubHandlers:
    """
    Contains handler methods for various GitHub webhook events.
    Each method processes the event payload and triggers Discord message updates.
    """
    def __init__(self, data_persistence, discord_bot):
        """
        Initializes the GitHubHandlers instance.

        Parameters:
        - data_persistence (DataPersistence): Instance for managing persistent data.
        - discord_bot (DiscordBot): Instance of the Discord bot.
        """
        self.data_persistence = data_persistence
        self.discord_bot = discord_bot
        self.EVENT_HANDLERS = {
            "push": self.handle_push,
            "check_run": self.handle_check_run,
            "check_suite": self.handle_check_suite,
            "workflow_run": self.handle_workflow_run,
            "workflow_job": self.handle_workflow_job,

            "pull_request": self.handle_pull_request,
            "pull_request_review": self.handle_pull_request_review,
            "pull_request_review_comment": self.handle_pull_request_review_comment,
            "issues": self.handle_issues,
            "issue_comment": self.handle_issue_comment,
            "create": self.handle_create,
            "delete": self.handle_delete,
            "fork": self.handle_fork,
            "release": self.handle_release,
            "watch": self.handle_watch,
            "member": self.handle_member,
            "public": self.handle_public,
            "repository": self.handle_repository,
            "commit_comment": self.handle_commit_comment,
        }

    def handle_event(self, event_type, payload):
        """
        Dispatches the incoming event to the appropriate handler.

        Parameters:
        - event_type (str): The type of the GitHub event.
        - payload (dict): The webhook payload.
        """
        handler = self.EVENT_HANDLERS.get(event_type)
        if handler:
            logging.info(f"Handling event: {event_type}")
            handler(payload)
        else:
            logging.warning(f"No handler found for event type: {event_type}")
            # Optionally handle unexpected events here

    def handle_push(self, payload):
        """
        Handles the 'push' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing push information.
        """
        commits = payload.get("commits", [])
        repo = payload.get("repository", {})
        repo_full_name = repo.get("full_name", "unknown/unknown")
        for commit in commits:
            sha = commit.get("id", "")
            message = commit.get("message", "")
            url = commit.get("url", "#")
            key = f"push:{sha}"
            commit_data = {
                "message": message,
                "url": url,
                "repo_full_name": repo_full_name
            }
            self.data_persistence.update_data_store(key, commit_data)
            asyncio.run_coroutine_threadsafe(
                self.discord_bot.send_or_edit(key, handler_name="push"),
                self.discord_bot.bot.loop
            )

    def handle_check_run(self, payload):
        """
        Handles the 'check_run' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing check run information.
        """
        check_run = payload.get("check_run", {})
        run_id = str(check_run.get("id", "unknown"))
        name = check_run.get("name", "Unnamed Check")
        url = check_run.get("html_url", "#")
        status = check_run.get("status", "unknown")
        conclusion = check_run.get("conclusion", "unknown")
        head_sha = check_run.get("head_sha", "unknown")
        repo_full_name = payload.get("repository", {}).get("full_name", "unknown/unknown")
        key = f"check_run:{run_id}"
        check_run_data = {
            "name": name,
            "url": url,
            "status": status,
            "conclusion": conclusion,
            "head_sha": head_sha,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, check_run_data)
        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="check_run"),
            self.discord_bot.bot.loop
        )

    def handle_check_suite(self, payload):
        """
        Handles the 'check_suite' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing check suite information.
        """
        check_suite = payload.get("check_suite", {})
        suite_id = str(check_suite.get("id", "unknown"))
        name = check_suite.get("name", "Unnamed Check Suite")
        url = check_suite.get("html_url", "#")
        status = check_suite.get("status", "unknown")
        conclusion = check_suite.get("conclusion", "unknown")
        head_sha = check_suite.get("head_sha", "unknown")
        repo_full_name = check_suite.get("repository", {}).get("full_name", "unknown/unknown")
        key = f"check_suite:{suite_id}"
        check_suite_data = {
            "name": name,
            "url": url,
            "status": status,
            "conclusion": conclusion,
            "head_sha": head_sha,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, check_suite_data)
        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="check_suite"),
            self.discord_bot.bot.loop
        )

    def handle_workflow_run(self, payload):
        """
        Handles the 'workflow_run' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing workflow run information.
        """
        workflow_run = payload.get("workflow_run", {})
        action = payload.get("action", "")

        if action != "completed":
            # Only process workflow runs that have completed
            logging.info(f"Ignored workflow_run action: {action}")
            return

        run_id = str(workflow_run.get("id", "unknown"))
        name = workflow_run.get("name", "Unnamed Workflow")
        status = workflow_run.get("status", "unknown")
        conclusion = workflow_run.get("conclusion", "unknown")
        url = workflow_run.get("html_url", "#")
        started_at = workflow_run.get("started_at", "")
        completed_at = workflow_run.get("completed_at", "")
        head_sha = workflow_run.get("head_sha", "unknown")
        repo_full_name = workflow_run.get("repository", {}).get("full_name", "unknown/unknown")

        key = f"workflow_run:{run_id}"
        workflow_run_data = {
            "name": name,
            "status": status,
            "conclusion": conclusion,
            "url": url,
            "started_at": started_at,
            "completed_at": completed_at,
            "head_sha": head_sha,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, workflow_run_data)
        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="workflow_run"),
            self.discord_bot.bot.loop
        )

    def handle_workflow_job(self, payload):
        """
        Handles the 'workflow_job' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing workflow job information.
        """
        workflow_job = payload.get("workflow_job", {})
        job_id = str(workflow_job.get("id", "unknown"))
        name = workflow_job.get("name", "Unnamed Workflow Job")
        url = workflow_job.get("html_url", "#")
        status = workflow_job.get("status", "unknown")
        conclusion = workflow_job.get("conclusion", "unknown")
        head_sha = workflow_job.get("head_sha", "unknown")
        repo_full_name = workflow_job.get("repository", {}).get("full_name", "unknown/unknown")

        key = f"workflow_job:{job_id}"
        workflow_job_data = {
            "name": name,
            "url": url,
            "status": status,
            "conclusion": conclusion,
            "head_sha": head_sha,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, workflow_job_data)
        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="workflow_job"),
            self.discord_bot.bot.loop
        )

    def handle_pull_request(self, payload):
        """
        Handles the 'pull_request' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing pull request information.
        """
        pr = payload.get("pull_request", {})
        action = payload.get("action", "unknown")
        pr_number = pr.get("number", 0)
        title = pr.get("title", "")
        url = pr.get("html_url", "#")
        merged = pr.get("merged", False)
        repo_full_name = payload.get("repository", {}).get("full_name", "unknown/unknown")

        key = f"pull_request:{pr_number}"
        pr_data = {
            "title": title,
            "url": url,
            "action": action,
            "merged": merged,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, pr_data)
        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="pull_request"),
            self.discord_bot.bot.loop
        )

    def handle_pull_request_review(self, payload):
        """
        Handles the 'pull_request_review' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing pull request review information.
        """
        review = payload.get("review", {})
        pr = payload.get("pull_request", {})
        pr_number = pr.get("number", 0)
        reviewer = review.get("user", {}).get("login", "unknown")
        url = review.get("html_url", "#")
        action = review.get("state", "commented")
        body = review.get("body", "")
        repo_full_name = payload.get("repository", {}).get("full_name", "unknown/unknown")

        key = f"pull_request_review:{pr_number}:{reviewer}:{url}"
        review_data = {
            "user": reviewer,
            "url": url,
            "action": action,
            "body": body,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, review_data)
        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="pull_request_review"),
            self.discord_bot.bot.loop
        )

    def handle_pull_request_review_comment(self, payload):
        """
        Handles the 'pull_request_review_comment' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing pull request review comment information.
        """
        comment = payload.get("comment", {})
        pr = payload.get("pull_request", {})
        pr_number = pr.get("number", 0)
        commenter = comment.get("user", {}).get("login", "unknown")
        comment_url = comment.get("html_url", "#")
        body = comment.get("body", "")
        repo_full_name = payload.get("repository", {}).get("full_name", "unknown/unknown")

        key = f"pull_request_review_comment:{pr_number}:{commenter}:{comment_url}"
        comment_data = {
            "user": commenter,
            "url": comment_url,
            "body": body,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, comment_data)
        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="pull_request_review_comment"),
            self.discord_bot.bot.loop
        )

    def handle_issues(self, payload):
        """
        Handles the 'issues' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing issue information.
        """
        issue = payload.get("issue", {})
        action = payload.get("action", "unknown")
        issue_number = issue.get("number", 0)
        title = issue.get("title", "")
        url = issue.get("html_url", "#")
        repo_full_name = payload.get("repository", {}).get("full_name", "unknown/unknown")

        key = f"issue:{issue_number}:{action}"
        issue_data = {
            "title": title,
            "url": url,
            "action": action,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, issue_data)
        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="issues"),
            self.discord_bot.bot.loop
        )

    def handle_issue_comment(self, payload):
        """
        Handles the 'issue_comment' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing issue comment information.
        """
        comment = payload.get("comment", {})
        issue = payload.get("issue", {})
        issue_number = issue.get("number", 0)
        commenter = comment.get("user", {}).get("login", "unknown")
        comment_url = comment.get("html_url", "#")
        body = comment.get("body", "")
        repo_full_name = payload.get("repository", {}).get("full_name", "unknown/unknown")

        key = f"issue_comment:{issue_number}:{commenter}:{comment_url}"
        comment_data = {
            "user": commenter,
            "url": comment_url,
            "body": body,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, comment_data)
        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="issue_comment"),
            self.discord_bot.bot.loop
        )

    def handle_create(self, payload):
        """
        Handles the 'create' event from GitHub (e.g., branch or tag creation).

        Parameters:
        - payload (dict): The webhook payload containing create event information.
        """
        ref_type = payload.get("ref_type", "unknown")  # Type of reference created (branch or tag)
        ref = payload.get("ref", "unknown")           # Name of the branch or tag

        # Attempt to extract 'sender', fallback to 'user' if 'sender' is missing
        sender_info = payload.get("sender", {})
        sender = sender_info.get("login") if sender_info else payload.get("user", "unknown")

        repo_full_name = payload.get("repository", {}).get("full_name", "unknown/unknown")

        if ref_type == "branch":
            ref_url = f"https://github.com/{repo_full_name}/tree/{ref}"
        elif ref_type == "tag":
            ref_url = f"https://github.com/{repo_full_name}/releases/tag/{ref}"
        else:
            ref_url = None  # Use None instead of "#"

        key = f"create:{ref}"  # Unique key based on the reference name
        create_data = {
            "ref_type": ref_type,
            "ref": ref,
            "user": sender,
            "ref_url": ref_url if ref_url else "",
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, create_data)

        logging.info(f"Handling create event: {ref_type} '{ref}' by {sender} in {repo_full_name}")

        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="create"),
            self.discord_bot.bot.loop
        )

    def handle_delete(self, payload):
        """
        Handles the 'delete' event from GitHub (e.g., branch or tag deletion).

        Parameters:
        - payload (dict): The webhook payload containing delete event information.
        """
        ref_type = payload.get("ref_type", "unknown")  # Type of reference deleted (branch or tag)
        ref = payload.get("ref", "unknown")           # Name of the branch or tag

        # Attempt to extract 'sender', fallback to 'user' if 'sender' is missing
        sender_info = payload.get("sender", {})
        sender = sender_info.get("login") if sender_info else payload.get("user", "unknown")

        repo_full_name = payload.get("repository", {}).get("full_name", "unknown/unknown")

        if ref_type == "branch":
            ref_url = f"https://github.com/{repo_full_name}/tree/{ref}"
        elif ref_type == "tag":
            ref_url = f"https://github.com/{repo_full_name}/releases/tag/{ref}"
        else:
            ref_url = None  # Use None instead of "#"

        key = f"delete:{ref}"  # Unique key based on the reference name
        delete_data = {
            "ref_type": ref_type,
            "ref": ref,
            "user": sender,
            "ref_url": ref_url if ref_url else "",
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, delete_data)

        logging.info(f"Handling delete event: {ref_type} '{ref}' by {sender} in {repo_full_name}")

        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="delete"),
            self.discord_bot.bot.loop
        )

    def handle_fork(self, payload):
        """
        Handles the 'fork' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing fork event information.
        """
        sender = payload.get("sender", {}).get("login", "unknown")  # User who forked the repository
        repository = payload.get("repository", {})
        repo_full_name = repository.get("full_name", "unknown/unknown")  # Original repository name
        forkee = payload.get("forkee", {})
        forkee_name = forkee.get("full_name", "unknown")  # Forked repository name
        forkee_url = forkee.get("html_url", "#")  # URL to the forked repository

        key = f"fork:{forkee_name}"  # Unique key based on the forked repository name
        fork_data = {
            "sender": sender,
            "repo_name": repo_full_name,
            "forkee_name": forkee_name,
            "forkee_url": forkee_url,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, fork_data)

        logging.info(f"Handling fork event: {sender} forked {repo_full_name} to {forkee_name}")

        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="fork"),
            self.discord_bot.bot.loop
        )

    def handle_release(self, payload):
        """
        Handles the 'release' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing release event information.
        """
        release = payload.get("release", {})
        action = payload.get("action", "unknown")  # Action on the release (e.g., "published", "deleted")
        name = release.get("name", "No Name")  # Name of the release
        url = release.get("html_url", "#")  # URL to the release
        publisher = payload.get("sender", {}).get("login", "unknown")  # User who published the release
        repo_full_name = payload.get("repository", {}).get("full_name", "unknown/unknown")

        key = f"release:{name}"  # Unique key based on the release name
        release_data = {
            "action": action,
            "name": name,
            "url": url,
            "publisher": publisher,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, release_data)

        logging.info(f"Handling release event: {action} release '{name}' by {publisher} in {repo_full_name}")

        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="release"),
            self.discord_bot.bot.loop
        )

    def handle_repository(self, payload):
        """
        Handles the 'repository' event from GitHub (e.g., repository creation or deletion).

        Parameters:
        - payload (dict): The webhook payload containing repository event information.
        """
        repo = payload.get("repository", {})
        action = payload.get("action", "unknown")  # Action on the repository (e.g., "created", "deleted")
        repo_name = repo.get("full_name", "unknown/unknown")  # Repository full name
        repo_url = repo.get("html_url", "#")  # URL to the repository
        owner = repo.get("owner", {}).get("login", "unknown")  # Owner of the repository

        key = f"repository:{repo_name}"  # Unique key based on the repository name
        repository_data = {
            "action": action,
            "name": repo_name,
            "url": repo_url,
            "owner": owner,
            "repo_full_name": repo_name
        }
        self.data_persistence.update_data_store(key, repository_data)

        logging.info(f"Handling repository event: {action} repository '{repo_name}' by {owner}")

        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="repository"),
            self.discord_bot.bot.loop
        )

    def handle_watch(self, payload):
        """
        Handles the 'watch' event from GitHub (e.g., starring a repository).

        Parameters:
        - payload (dict): The webhook payload containing watch event information.
        """
        action = payload.get("action", "starred")  # Action performed (e.g., "starred", "unstarred")
        sender = payload.get("sender", {}).get("login", "unknown")  # User who performed the action
        repository = payload.get("repository", {})
        repo_full_name = repository.get("full_name", "unknown/unknown")  # Repository name
        repo_url = repository.get("html_url", "#")  # URL to the repository

        key = f"watch:{sender}:{repo_full_name}"  # Unique key based on user and repository
        watch_data = {
            "action": action,
            "user": sender,
            "repo_name": repo_full_name,
            "repo_url": repo_url,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, watch_data)

        logging.info(f"Handling watch event: {sender} {action} repository '{repo_full_name}'")

        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="watch"),
            self.discord_bot.bot.loop
        )

    def handle_member(self, payload):
        """
        Handles the 'member' event from GitHub (e.g., adding or removing a collaborator).

        Parameters:
        - payload (dict): The webhook payload containing member event information.
        """
        member = payload.get("member", {})
        member_login = member.get("login", "unknown")
        action = payload.get("action", "unknown")  # e.g., "added", "removed"
        repo_full_name = payload.get("repository", {}).get("full_name", "unknown/unknown")
        repo_url = payload.get("repository", {}).get("html_url", "#")  # Repository URL

        key = f"member:{member_login}:{repo_full_name}:{action}"  # Unique key based on member and action
        member_data = {
            "member_login": member_login,
            "action": action,
            "repo_full_name": repo_full_name,
            "repo_url": repo_url
        }
        self.data_persistence.update_data_store(key, member_data)

        logging.info(f"Handling member event: {action} '{member_login}' in {repo_full_name}")

        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="member"),
            self.discord_bot.bot.loop
        )

    def handle_commit_comment(self, payload):
        """
        Handles the 'commit_comment' event from GitHub.

        Parameters:
        - payload (dict): The webhook payload containing commit comment information.
        """
        comment = payload.get("comment", {})
        commit_sha = comment.get("commit_id", "unknown")
        commenter = comment.get("user", {}).get("login", "unknown")
        comment_url = comment.get("html_url", "#")
        body = comment.get("body", "")
        repo_full_name = payload.get("repository", {}).get("full_name", "unknown/unknown")

        key = f"commit_comment:{commit_sha}:{commenter}:{comment_url}"  # Unique key based on commit and commenter
        commit_comment_data = {
            "commit_sha": commit_sha,
            "commenter": commenter,
            "url": comment_url,
            "body": body,
            "repo_full_name": repo_full_name
        }
        self.data_persistence.update_data_store(key, commit_comment_data)

        logging.info(f"Handling commit_comment event: {commenter} commented on commit '{commit_sha}' in {repo_full_name}")

        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="commit_comment"),
            self.discord_bot.bot.loop
        )

    def handle_public(self, payload):
        """
        Handles the 'public' event from GitHub (e.g., repository made public).

        Parameters:
        - payload (dict): The webhook payload containing public event information.
        """
        action = payload.get("action", "made public")  # Action performed (e.g., "made public")
        repository = payload.get("repository", {})
        repo_full_name = repository.get("full_name", "unknown/unknown")
        repo_url = repository.get("html_url", "#")
        sender = payload.get("sender", {}).get("login", "unknown")  # User who performed the action

        key = f"public:{repo_full_name}"  # Unique key based on repository name
        public_data = {
            "action": action,
            "repo_full_name": repo_full_name,
            "repo_url": repo_url,
            "sender": sender
        }
        self.data_persistence.update_data_store(key, public_data)

        logging.info(f"Handling public event: Repository '{repo_full_name}' {action} by {sender}")

        asyncio.run_coroutine_threadsafe(
            self.discord_bot.send_or_edit(key, handler_name="public"),
            self.discord_bot.bot.loop
        )
