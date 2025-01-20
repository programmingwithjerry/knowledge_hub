#!/usr/bin/env python3
"""
Fetch and list all available course titles from a paginated or flat API.
Automatically enroll in all courses using provided credentials.
"""

import requests

# The base URL for the API that provides the course data
base_url = 'http://127.0.0.1:8000/api/'

# The specific URL endpoint to fetch courses
url = f'{base_url}courses/'

# Initialize an empty list to store the titles of available courses
available_courses = []

# User credentials for enrollment
username = "alex"  # Replace with your username
password = "IsezuoAlbert"  # Replace with your password

# Loop to continue fetching courses as long as there is a next page (pagination)
while url is not None:
    # Print a message indicating that the program is loading courses from the current URL
    print(f'Loading courses from {url}')

    # Make a GET request to the current URL to fetch course data
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raise an exception for HTTP errors
        response = r.json()  # Parse the JSON response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        break
    except ValueError:
        print("Failed to parse JSON response.")
        break

    # Initialize an empty list for courses in the current response
    courses = []

    # Determine response type and process accordingly
    if isinstance(response, dict):
        # Paginated response expected
        url = response.get('next')  # Get the URL for the next page of results
        courses = response.get('results', [])  # Extract the list of courses
        available_courses += [course.get('title', 'Untitled') for course in courses]
    elif isinstance(response, list):
        # Flat response (no pagination)
        courses = response  # Entire response is the list of courses
        available_courses += [item.get('title', 'Untitled') for item in response]
        url = None  # No pagination, stop the loop
    else:
        print(f"Unexpected response format: {response}")
        break

    # Loop through the courses to enroll in each
    for course in courses:
        # Extract the course ID and title from the course data
        course_id = course['id']  # The unique identifier for the course
        course_title = course['title']  # The title of the course

        # Make a POST request to enroll in the course
        try:
            r = requests.post(
                f'{base_url}courses/{course_id}/enroll/',
                auth=(username, password)  # Use basic authentication
            )
            if r.status_code == 200:
                # Successful request
                print(f'Successfully enrolled in {course_title}')
            else:
                # Unsuccessful enrollment, print the error response
                print(f'Failed to enroll in {course_title}: {r.status_code} - {r.reason}')
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during enrollment in {course_title}: {e}")

# Print out the list of available courses
print(f'Available courses: {", ".join(available_courses)}')

