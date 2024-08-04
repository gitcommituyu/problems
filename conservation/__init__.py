"""
Módulo de verificación para el problema de conservación de arte.
"""

import re
import csv
import check50

@check50.check()
def exists():
    """transcript.txt existe."""
    check50.exists("transcript.txt")
    check50.include("solutions.csv")

@check50.check(exists)
def formatting():
    """transcript.txt formateado correctamente"""
    solutions = read_solutions("solutions.csv")
    answers = read_answers("transcript.txt")

    for question in solutions.keys():
        regex = re.compile(
            r"\s*".join([re.escape(word) for word in question.split()]) + r"?\s*"
        )
        matches = list(filter(regex.search, answers))
        if len(matches) != 1:
            raise check50.Failure("transcript.txt está incorrectamente formateado")

@check50.check(formatting)
def primer_art():
    """Primer artículo transcrito correctamente"""
    solutions = read_solutions("solutions.csv")
    answers = read_answers("transcript.txt")

    for question in list(
        filter(lambda question: "i." in question, solutions.keys())
    ):
        solution = solutions[question]
        if not check_answers(question, solution, answers):
            raise check50.Failure(
                "El primer artículo no fue transcrito correctamente"
            )
        
def check_answers(question: str, solution: str, answers: list[str]) -> bool:
    """
    Checks list of student answers for solution to given question

    Args:
        question (str): the question to check
        solution (str): the solution to the question
        answers (list[str]): the list of student answers

    Returns:
        (bool) whether the student's list of answers contains the correct answer to the given question
    """
    # decode solution from hex
    solution = bytes.fromhex(solution).decode("utf-8")

    # construct regex
    regex = re.compile(
        r"\s*".join([re.escape(word) for word in question.split()])
        + r":\s*"
        + re.escape(solution)
    )

    # check for matching answers
    if len(list(filter(regex.search, answers))) != 1:
        return False
    return True


def read_answers(filename: str) -> list[str]:
    """
    Reads the student's answers file

    Args:
        filename (str): the name of the filename containing the student's answers

    Returns:
        (list[str]): a list of lines on which the student has written answers

    Raises:
        FileNotFoundError
    """
    with open(filename, "r") as f:
        # read and keep only the non-whitespace lines
        return list(
            answer.lower()
            for answer in filter(lambda s: not s.isspace(), f.readlines())
        )


def read_solutions(filename: str) -> dict:
    """
    Reads the accompanying solutions CSV file into a dictionary in which questions are keys and solutions are values

    Args:
        filename (str): the name of the CSV file containing question and solutions

    Returns:
        (dict): a dictionary in which questions are keys and solutions are values

    Raises:
        FileNotFoundError
    """
    if not filename.endswith(".csv"):
        return {}

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        solutions = {}
        for row in reader:
            try:
                question = row["question"].lower()
                solution = row["answer"]
            except KeyError:
                check50.log("solutions.csv is not properly formatted")
                break

            solutions[question] = solution

    return solutions