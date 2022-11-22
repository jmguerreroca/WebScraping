# Librerías
import time
import re
import argparse
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup, NavigableString
from selenium.webdriver.common.by import By
from distutils.log import error
from tqdm import tqdm

SUBJECT_HELP = """
    You need to enter one of these numerical codes:

    00 - General
    01 - History and biography
    03 - Mathematical logic and foundations
    05 - Combinatorics
    06 - Order, lattices, ordered algebraic structures
    08 - General algebraic systems
    11 - Number theory
    12 - Field theory and polynomials
    13 - Commutative rings and algebras
    14 - Algebraic geometry
    15 - Linear and multilinear algebra; matrix theory
    16 - Associative rings and algebras
    17 - Non-associative rings and algebras
    18 - Category theory, homological algebra
    19 - K-theory
    20 - Group theory and generalizations
    22 - Topological groups, Lie groups
    26 - Real functions
    28 - Measure and integration
    30 - Functions of a complex variable
    31 - Potential theory
    32 - Several complex variables and analytic spaces
    33 - Special functions
    34 - Ordinary differential equations
    35 - Partial differential equations
    37 - Dynamical systems and ergodic theory
    39 - Finite differences and functional equations
    40 - Sequences, series, summability
    41 - Approximations and expansions
    42 - Fourier analysis
    43 - Abstract harmonic analysis
    44 - Integral transforms, operational calculus
    45 - Integral equations
    46 - Functional analysis
    47 - Operator theory
    49 - Calculus of variations and optimal control
    51 - Geometry
    52 - Convex and discrete geometry
    53 - Differential geometry
    54 - General topology
    55 - Algebraic topology
    57 - Manifolds and cell complexes
    58 - Global analysis, analysis on manifolds
    60 - Probability theory and stochastic processes
    62 - Statistics
    65 - Numerical analysis
    68 - Computer science
    70 - Mechanics of particles and systems
    74 - Mechanics of deformable solids
    76 - Fluid mechanics
    78 - Optics, electromagnetic theory
    80 - Classical thermodynamics, heat transfer
    81 - Quantum Theory
    82 - Statistical mechanics, structure of matter
    83 - Relativity and gravitational theory
    85 - Astronomy and astrophysics
    86 - Geophysics
    90 - Operations research, mathematical programming
    91 - Game theory, economics, social and behavioral sciences
    92 - Biology and other natural sciences
    93 - Systems theory; control
    94 - Information and communication, circuits
    97 - Mathematics education
"""

YEAR_HELP = """
    Year in which the doctoral thesis was handed in.
"""

COUNTRY_HELP = """
    Name of a country in English is required.
"""

URL = 'https://www.genealogy.math.ndsu.nodak.edu/'

# COLLECT INFORMATION ON EACH PhD:
def doctor(driver, id):

    # READING THE PAGE
    pth = f'{URL}id.php?id={id}'
    driver.get(pth)
    soup = BeautifulSoup(driver.page_source, features="lxml")

    # WEB SCRAPING
    main_cont = soup.find(id='mainContent')

    # AUTHOR NAME
    name = main_cont.find('h2').get_text().strip()

    # AUTHOR UNIVERSITY
    university = main_cont.find_next(
        'span').find_next('span').get_text()

    # YEAR OF PhD PUBLICATION
    year = main_cont.find('span').get_text()
    year = ''.join(re.findall(r"\d{4}$", year))

    # COUNTRY NAME
    if main_cont.find('img'):
        country = main_cont.find('img').get('title')
    else:
        country = ''

    for div in range(0, len(main_cont.find_all('div'))):
        # PhD TITLE
        if div == 3:
            title = ''.join([i if type(i) == NavigableString else '' for i in main_cont.
                            find_all('div')[3].contents[2].contents]).strip()
        # PhD SUBJET
        if div == 4:
            try:
                subject = main_cont.find_all('div')[div].get_text().split(r":", 1)[1].strip()
            except:
                subject = ''

    # MENTORS
    mentors_txt = re.search(r'Advisor.*', main_cont.get_text())
    if mentors_txt is not None:
        mentors_txt = mentors_txt.group(0)
        pre_mentors = re.split(r"No students known.", mentors_txt)[0]
        mentors = re.split(r"Advisor: |Advisor \d: ", pre_mentors)[1:]
    else:
        mentors = []

    # STUDENTS
    students = []
    if main_cont.table != None:
        students_searched = main_cont.table.find_all('a')
        for stud in students_searched:
            students.append(stud.get_text())

    return {
        'author': name,
        'PhD publication year': year,
        'university name': university,
        'country name': country,
        'PhD title': title,
        'subject': subject,
        'number of mentors': len(mentors),
        'mentors': mentors,
        'number of students': len(students),
        'students': students
    }

def main(subject, year, country):

    # NAVIGATION OPTIONS
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)

    # START THE WEB BROWSER
    start_time = float(time.time())
    driver.get(URL)
    con_time = float(time.time()) - start_time

    # CHECKING USER AGENTS
    agent = driver.execute_script("return navigator.userAgent")
    print(f"Chrome user agents: {agent}")

    # IF IT TAKES MORE THAN 1 MINUTE TO CONNECT, WE ABORT CONNECTION TO AVOID SATURATING THE SERVER
    if con_time > 60:
        error('The server is very busy right now, try again later.')

    print(f'Connection established in {con_time} seconds')

    advance_search = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/ul/li[2]/a')
    print(advance_search)
    advance_search.click()

    if subject:
        subject_search = driver.find_element(By.XPATH, f'//option[@value="{subject}"]')
        subject_search.click()

    if year:
        year_search = driver.find_element(By.ID, 'year')
        year_search.send_keys(year)

    if country:
        country_search = driver.find_element(By.NAME, 'country')
        country_search.send_keys(country)


    search_b = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div[2]/div/div[2]/div/form/div/table/tbody/tr[9]/td/input[1]')
    search_b.click()

    soup = BeautifulSoup(driver.page_source, features="lxml")
    table = soup.find(id='mainContent').table
    authors = table.find_all('tr')

    ids = []
    for author in authors:
        url = author.find('a').get('href')
        id = re.search('id=(.*)', url).group(1)
        ids.append(id)

    print(f'Your search has found {len(ids)} records in the database')

    i = 0
    authors_info = []
    for _ in tqdm(range(len(ids))):
        authors_info.append(doctor(driver, ids[i]))
        i += 1
        time.sleep(0.001)

    result = pd.DataFrame(authors_info)
    print(result.head(5))

    result.to_csv('../dataset/historical_spanish_PhD_computer_scientist.csv')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=str, help=SUBJECT_HELP)
    parser.add_argument("--year", type=str, help=YEAR_HELP)
    parser.add_argument("--country", type=str, help=COUNTRY_HELP)
    args = parser.parse_args()

    if args.subject is not None or args.year is not None or args.country is not None:
        main(args.subject, args.year, args.country)
    else:
        print('ERROR: At least one parameter should be provided to perform our web scraping')
        print("Let's run with default options: --country spain --subjet 68 (computer science)")
        main('68', None, 'spain')

