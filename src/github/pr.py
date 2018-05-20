import os
from collections import defaultdict
import requests # pip install 
import crayons # get from pypi
import json
import jinja2

pagination = "null"
query = """
query($orderBy: LanguageOrder!, $pagination: String) { 
  viewer {    
    name
    pullRequests(first: 100, after: $pagination, states: MERGED) {
      totalCount
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        url
        state
        additions
        deletions
        author {
          login
        }
        repository {
          nameWithOwner
        }
        createdAt
        repository {
          stargazers {
            totalCount
          }
          languages(first: 3, orderBy: $orderBy) {
            nodes {              
              name
            }
          }
        }
      }
    }
  }
}
"""

# Add repo owner names as a JSON array. E.g. if you don't want to include friends or organizations that you made some hobby projects with.
blacklist_json = os.environ['BLACKLIST']

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
blacklist = set(json.loads(blacklist_json)) 

variables = {
  "orderBy": {
    "field": "SIZE",
    "direction": "DESC"
  }  
}

pullrequests = []

pagination = ""
while True:
    resp = requests.post(GITHUB_GRAPHQL_URL, \
            json={"query": query, "variables": variables}, \
            headers={"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"})
    data = resp.json()

    pullrequests += data["data"]["viewer"]["pullRequests"]["nodes"]
    if not data["data"]["viewer"]["pullRequests"]["pageInfo"]["hasNextPage"]:
        break    
    variables["pagination"] =  data["data"]["viewer"]["pullRequests"]["pageInfo"]["endCursor"]
    
  
contributions = defaultdict(list)


for pullrequest in pullrequests:
    contributions[pullrequest["repository"]["nameWithOwner"]].append(pullrequest)

    
summaries = []
for repo, prs in contributions.items():
    repoOwner = repo.split('/')[0]
    if repoOwner in blacklist:
        continue
    
    additions = sum(pr["additions"] for pr in prs)
    deletions = sum(pr["deletions"] for pr in prs)
    stars = prs[0]["repository"]["stargazers"]["totalCount"]
    languages = "/".join(map(lambda i: i["name"], prs[0]["repository"]["languages"]["nodes"]))

    latex_characters = "&%$#_{}~^\\"    
    translation = dict(list(map(lambda c: (ord(c), '\\' + c), latex_characters)))
    # print(translation)
    summaries.append({
        'repo': repo.translate(translation),
        'additions': additions,
        'deletions': deletions,
        'stars': stars,
        'languages': languages.translate(translation),
        'prs': len(prs)
    })

summaries = sorted(summaries, key=lambda i: i["stars"], reverse=True)

# for summary in sorted(summaries, key=lambda i: i["stars"], reverse=True):
#     locals().update(summary)
#     print(repo.ljust(60), \
#         str(languages).ljust(50), \
#         crayons.green(f'+{additions}').ljust(7), \
#         crayons.red(f'-{deletions}').ljust(7), \
#         str(prs).ljust(5), \
#         crayons.yellow(f'⭐ {stars}').ljust(7))

env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'), trim_blocks=True, block_start_string='<<',block_end_string='>>',variable_start_string='<=', variable_end_string='=>')

template = env.get_template('pull_requests_template.tex')
print(template.render(prs=summaries))