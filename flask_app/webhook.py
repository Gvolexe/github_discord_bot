# flask_app/webhook.py

import hmac
import hashlib
import json
import logging
from flask import Flask, request, abort

def create_flask_app(config, data_persistence, github_handlers):
    """
    Factory function to create and configure the Flask application.

    Parameters:
    - config (Config): Configuration instance.
    - data_persistence (DataPersistence): Data persistence instance.
    - github_handlers (GitHubHandlers): GitHub event handlers.

    Returns:
    - Flask: The configured Flask application.
    """
    app = Flask(__name__)

    def verify_signature(req):
        """
        Verifies the GitHub webhook signature to ensure the request is legitimate.

        Parameters:
        - req (flask.Request): The incoming Flask request.

        Returns:
        - bool: True if the signature is valid or no secret is set, False otherwise.
        """
        if not config.GITHUB_WEBHOOK_SECRET:
            # If no secret is set, skip verification
            return True
        signature = req.headers.get('X-Hub-Signature-256')
        if not signature:
            return False
        try:
            sha_name, received_sig = signature.split('=')
        except ValueError:
            return False
        if sha_name != 'sha256':
            return False
        mac = hmac.new(
            config.GITHUB_WEBHOOK_SECRET.encode(),
            msg=req.data,
            digestmod='sha256'
        )
        expected_sig = mac.hexdigest()
        return hmac.compare_digest(received_sig, expected_sig)

    @app.route("/github-webhook", methods=['POST'])
    def github_webhook():
        """
        The endpoint that GitHub sends webhook events to.

        Returns:
        - Tuple[str, int]: A simple "OK" response with HTTP status 200 upon successful processing.

        Raises:
        - 403 Forbidden: If the signature verification fails.
        """
        if not verify_signature(request):
            logging.warning("Invalid signature for incoming webhook.")
            abort(403, "Invalid signature")

        event_type = request.headers.get('X-GitHub-Event', 'unknown')
        payload = request.json or {}

        logging.info(f"Received event: {event_type}")
        logging.debug(f"Payload: {json.dumps(payload, indent=2)}")

        try:
            github_handlers.handle_event(event_type, payload)
        except Exception as e:
            logging.error(f"Error handling event '{event_type}': {e}")
            # Optionally, implement error handling here

        return "OK", 200

    return app
