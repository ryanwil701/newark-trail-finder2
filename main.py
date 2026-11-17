from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

set_website_title("Ryan's Test Website")
set_site_information(
    author="Ryan Wilgus",
    description="Finds hiking trails for citizens of Newark, Delaware",
    sources="Drafter docs",
    planning="",
    links=["https://github.com/ryanwil701/newark-trail-finder2/"])

hide_debug_information()
set_website_framed(False)


@dataclass
class Trail:
    name: str
    drive_distance: int   # miles from campus
    difficulty: float     # 0.0 is a stroll, 1.0 is brutal
    length: float         # miles
    reviews: list[str]


@dataclass
class State:
    trails: list[Trail]
    max_drive: int
    difficulty: float
    trail_review: str


# distances are a rough estimate
starting_trails = [
    Trail("White Clay Creek State Park", 3, 0.3, 3.0, []),
    Trail("Middle Run Valley", 3, 0.5, 4.0, []),
    Trail("Iron Hill Park", 3, 0.5, 3.5, []),
    Trail("Lums Pond State Park", 10, 0.3, 6.0, []),
    Trail("Brandywine Creek State Park", 20, 0.8, 5.0, [])]

#add more trails later
DRIVE_OPTIONS = ["5", "10", "25"]
DIFFICULTY_OPTIONS = ["0.0", "0.1", "0.2", "0.3", "0.4", "0.5",
                      "0.6", "0.7", "0.8", "0.9", "1.0"]


def find_matches(state: State) -> list[Trail]:
    # keep trails that are close enough and not harder than what the user wants
    matches = []
    for trail in state.trails:
        if trail.drive_distance <= state.max_drive:
            if trail.difficulty <= state.difficulty:
                matches.append(trail)
    return matches


@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Newark Hike Finder"),
        "Got a free afternoon? Find a trail near UD or tell everyone about one you've hiked.",
        Button("Find a trail", search_page),
        Button("Leave a review", trail_review)])
    
@route
def search_page(state: State) -> Page:
    return Page(state, [
        Header("Find a Trail"),
        "How far are you up for driving? (miles)",
        SelectBox("max_drive", DRIVE_OPTIONS, str(state.max_drive)),
        "How tough of a hike do you want? (0.0 = easy stroll, 1.0 = leg day)",
        SelectBox("difficulty", DIFFICULTY_OPTIONS, str(state.difficulty)),
        Button("Show me trails", submit_search),
        Button("Back", index)])


@route
def submit_search(state: State, max_drive: str, difficulty: str) -> Page:
    state.max_drive = int(max_drive)
    state.difficulty = float(difficulty)
    if len(find_matches(state)) == 0:
        return no_results(state)
    return results(state)


@route
def results(state: State) -> Page:
    lines = []
    for trail in find_matches(state):
        lines.append(trail.name + ": " + str(trail.drive_distance) + " mi away, "
                     + str(trail.length) + " mi long, difficulty "
                     + str(trail.difficulty) + " (" + str(len(trail.reviews)) + " reviews)")
    return Page(state, [
        Header("Here's what we found"),
        "These trails fit what you're looking for:",
        NumberedList(lines),
        Button("Search again", search_page),
        Button("Home", index)])


@route
def no_results(state: State) -> Page:
    return Page(state, [
        Header("No trails found"),
        "Nothing matched that search. Try driving a little farther or bumping up the difficulty.",
        Button("Search again", search_page),
        Button("Home", index)])


@route
def trail_review(state: State) -> Page:
    trail_names = []
    for trail in state.trails:
        trail_names.append(trail.name)
    return Page(state, [
        Header("Leave a Review"),
        "Which trail did you hike?",
        SelectBox("trail_name", trail_names, trail_names[0]),
        "How was it?",
        TextArea("review_text", state.trail_review),
        Button("Post review", submit_review),
        Button("Back", index)])


@route
def submit_review(state: State, trail_name: str, review_text: str) -> Page:
    if review_text.strip() == "":
        return Page(state, [
            "Looks like your review is empty. Write a little something first!",
            Button("Back", trail_review)
        ])
    for trail in state.trails:
        if trail.name == trail_name:
            trail.reviews.append(review_text)
    state.trail_review = ""
    return Page(state, [
        "Thanks! Your review of " + trail_name + " is posted.",
        Button("Home", index)])


# the tests
test_state = State(starting_trails, 10, 0.3, "")
assert_equal(index(test_state), Page(test_state, [
    Header("Newark Hike Finder"),
    "Got a free afternoon? Find a trail near UD or tell everyone about one you've hiked.",
    Button("Find a trail", search_page),
    Button("Leave a review", trail_review)]))

# within 5 miles and up to 0.5 difficulty: White Clay, Middle Run, Iron Hill
assert_equal(len(find_matches(State(starting_trails, 5, 0.5, ""))), 3)

# nothing is within 1 mile
assert_equal(len(find_matches(State(starting_trails, 1, 1.0, ""))), 0)

start_server(State(starting_trails, 10, 0.3, ""))
