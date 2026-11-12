from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

set_webiste_title("Ryan's Test Website")
set_site_information(
    author="Ryan Wilgus",
    description="Finds hiking trails for citizens of Newark, Delaware",
    soutces="Drafter docs",
    planning="",
    links=["https://github.com/ryanwil701/newark-trail-finder2/"]

hide_debug_information()
set_website_framed(False)


@dataclass
class Trail:
    name: str
    drive_distance: int
    difficulty: float
    length: float
    reviews: list[str]
@dataclass
class State:
    trails: list[Trails]
    max_drive: int
    difficulty: float
    trail_review: str

starting_trails = [
    Trail("White Clay Creek State Park", 3, 0.3, 3.0, []),
    Trail("Middle Run Valley", 3, 0.5, 4.0, []),
    Trail("Iron Hill Park", 3, 0.5, 3.5, []),
    Trail("Lums Pond State Park", 10, 0.3, 6.0, []),
    Trail("Brandywine Creek Sate Park", 20, 0.8, 5.0, [])
]

    
@route
def index(state: State) -> Page:
    return Page(state, [Header("Newark Hike Finder"),
                       "Welcome! Find a trail near campus or leave a review.",
                       Button("Search", search_page),
                       Button("Review", trail_review)
                       ])

assert_equal(index(State()), Page(State(), ["Hello World!"]))

start_server(State([], 0, 0.0, ""))
