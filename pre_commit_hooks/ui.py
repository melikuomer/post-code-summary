from typing import List
from collections import Counter
import os
from pre_commit_hooks.model import Artifact
from pre_commit_hooks.notification import send_notification

def generate_html(artifact: Artifact) -> None:
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Code Feedback Details</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            h1 {
                color: #2c3e50;
                text-align: center;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            .feedback-card {
                background: white;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .line-number {
                color: #e74c3c;
                font-size: 1.2em;
                margin: 0;
            }
            .feedback-type {
                display: inline-block;
                padding: 5px 10px;
                background: #3498db;
                color: white;
                border-radius: 4px;
                font-size: 0.9em;
            }
            .code-block {
                background: #f8f9fa;
                padding: 10px;
                border-radius: 4px;
                font-family: monospace;
                border-left: 4px solid #2ecc71;
            }
            .feedback-text {
                color: #34495e;
                line-height: 1.6;
            }
        </style>
    </head>
    <body>
    <h1>Code Feedback Details</h1>
    """
    # Add overview section
    overview_content = f"""
    <div class="feedback-card">
        <h2>Overview</h2>
        <p class="feedback-text">
        <p style="color: #e74c3c;">🚫 Blunders: {sum(1 for x in artifact.feedbacks if x.type.value == 'blunder')}</p>
        <p style="color: #f1c40f;">⚠️ Missed Wins: {sum(1 for x in artifact.feedbacks if x.type.value == 'missed_win')}</p>
        <p style="color: #3498db;">💡 Improvements: {sum(1 for x in artifact.feedbacks if x.type.value == 'improvement')}</p>
        <p style="color: #2ecc71;">✨ Brilliant Moves: {sum(1 for x in artifact.feedbacks if x.type.value == 'brilliant')}</p>
        <p style="color: #9b59b6;">❗ Book Moves: {sum(1 for x in artifact.feedbacks if x.type.value == 'book_move')}</p>
        </p>
    </div>
    """
    html_content += overview_content
    # Sort feedbacks by file name first, then line number
    sorted_feedbacks = sorted(artifact.feedbacks, key=lambda x: (getattr(x, 'file_name', ''), x.line_number))

    for feedback in sorted_feedbacks:
        html_content += f"""
        <div class="feedback-card">
        <h3 class="file-name">Line {feedback.file_name}</h3>
            <h3 class="line-number">Line {feedback.line_number}</h3>
            <span class="feedback-type" style="background-color: {
                {
                    'blunder': '#e74c3c',
                    'missed_win': '#f1c40f',
                    'improvement': '#3498db',
                    'brilliant': '#2ecc71',
                    'book_move': '#9b59b6'
                }.get(feedback.type.value, '#3498db')
            }">{
                {
                'blunder': '🚫',
                'missed_win': '⚠️',
                'improvement': '💡',
                'brilliant': '✨',
                'book_move': '❗'
            }.get(feedback.type.value, '')} {feedback.type.value}</span>
            <div class="code-block">{feedback.line_text}</div>
            <p class="feedback-text">{feedback.feedback}</p>
        </div>
        """

    html_content += "</body></html>"

    with open("feedback.html", "w") as f:
        f.write(html_content)

def display_artifact(artifact: Artifact) -> None:
    # Count feedback types
    feedback_counts = Counter(feedback.type.value for feedback in artifact.feedbacks)

    # Create summary message
    summary = ", ".join(f"{count} {feedback_type}" for feedback_type, count in feedback_counts.items())

    # Send single notification with summary
    send_notification("Code Feedback Summary", summary)

    # Generate HTML
    generate_html(artifact)

    # Open file directly
    import webbrowser
    webbrowser.open('file://' + os.path.realpath("feedback.html"))

if __name__ == "__main__":
    # Create a test artifact
    from model import Feedback, FeedbackType
    feedbacks: List[Feedback]= []
    test_feedback = Feedback(
        line_number=1,
        line_text="def example():",
        type=FeedbackType.blunder,
        feedback="Missing docstring"
    )
    feedbacks.append(test_feedback)

    test_feedback2 = Feedback(
        line_number=5,
        line_text="return x + y",
        type=FeedbackType.missed_win,
        feedback="Variables not defined"
    )
    feedbacks.append(test_feedback2)

    test_artifact = Artifact(feedbacks=feedbacks)
    # Display test artifact
    display_artifact(test_artifact)
