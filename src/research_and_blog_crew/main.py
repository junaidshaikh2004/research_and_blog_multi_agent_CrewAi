from research_and_blog_crew.crew import ResearchAndBlogCrew


def run(topic: str | None = None):
    """
    Run the crew.
    """
    if topic is None:
        topic = input("Enter a topic for the report and blog: ").strip()

    inputs = {
        'topic': topic
    }

    try:
        ResearchAndBlogCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


