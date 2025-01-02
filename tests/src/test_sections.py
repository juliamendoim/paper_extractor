import pytest

from src.sections import matching_section, section_pages

@pytest.fixture()
def section_examples():
    def _section_examples(example):
        examples_dict = {
            "oe_lvl_1": (
                [[1,'2. Study objective and study endpoints',51],
                 [2,'2.1. Study objectives',51],
                 [2,'2.2. Study endpoints',52],
                 [1,'3. Study design',54]],
                [True,True,True,False],
                [51,52]
            ),
            "o_lvl1_e": (
                [[1,'8 STUDY OBJECTIVES',33],
                 [2,'8.1 Primary Objective',33],
                 [2,'8.2 Secondary Objectives',33],
                 [2,'8.3 Exploratory Objectives',34],
                 [1,'9 INVESTIGATIONAL PLAN',34],
                 [2,'9.1 Overall Study Design and Plan',34],
                 [3,'9.1.1 Primary Endpoint',35],
                 [3,'9.1.2 Secondary Endpoints',35],
                 [3,'9.1.3 Exploratory Endpoints',35]],
                [True,True,True,True,False,False,True,True,True],
                [33,34,35]
            ),
            "o_noe": (
                [[1,'8 STUDY OBJECTIVES',33],
                 [2,'8.1 Primary Objective',33],
                 [2,'8.2 Secondary Objectives',33],
                 [2,'8.3 Exploratory Objectives',34],
                 [1,'9 INVESTIGATIONAL PLAN',34]],
                [True,True,True,True,False],
                [33,34]
            ),
            "e_noo": (
                [[1,'9 INVESTIGATIONAL PLAN',34],
                 [2,'9.1 Overall Study Design and Plan',34],
                 [3,'9.1.1 Primary Endpoint',35],
                 [3,'9.1.2 Secondary Endpoints',35],
                 [3,'9.1.3 Exploratory Endpoints',35],
                 [2,'9.2 Randomization',35],
                 [1,'10 SELECTION OF STUDY POPULATION',36]],
                [False,False,True,True,True,False,False],
                [35]
            ),
            "no_sections": (
                [[1,'5 TABLE OF CONTENTS',19],
                 [1,'6 DEFINITIONS OF TERMS',26],
                 [1,'7 INTRODUCTION',28]],
                [False,False,False],
                []
            )
        }

        return examples_dict[example]

    return _section_examples


@pytest.mark.parametrize(
    "example",
    [
        "oe_lvl_1",
        "o_lvl1_e",
        "o_noe",
        "e_noo",
        "no_sections"
    ]
)
def test_matching_section(section_examples,example):
    example_case = section_examples(example)
    sections = [section[1] for section in example_case[0]]
    expected = example_case[1]
    predictions = [matching_section(section) for section in sections]
    assert predictions == expected

@pytest.mark.parametrize(
    "example",
    [
        "oe_lvl_1",
        "o_lvl1_e",
        "o_noe",
        "e_noo",
        "no_sections"
    ]
)
def test_section_pages(section_examples, example):
    example_case = section_examples(example)
    sections = example_case[0]
    expected_pages = example_case[2]
    matched_pages = section_pages(sections)
    assert matched_pages == expected_pages
