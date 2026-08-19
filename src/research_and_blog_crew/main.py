from research_and_blog_crew.crew import ResearchAndBlogCrew


def run(topic:str):
    """
    Run the crew.
    """
    inputs = {
        'topic': topic
    }

    try:
        ResearchAndBlogCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


