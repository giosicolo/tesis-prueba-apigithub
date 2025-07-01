#!/usr/bin/env python
# coding: utf-8

# In[14]:


import requests


# In[10]:


# Metodo para obtener los metadatos generales de un repositorio de github con su API :
def getMetadata(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        metadata = {
            "full_name": data.get("full_name"),
            "description": data.get("description"),
            "clone_url": data.get("clone_url"),
            "stargazers_count": data.get("stargazers_count"),
            "forks_count": data.get("forks_count"),
            "open_issues_count": data.get("open_issues_count"),
            "default_branch": data.get("default_branch"),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at"),
            "pushed_at": data.get("pushed_at"),
            "language": data.get("language"),
            "license": data.get("license")["name"] if data.get("license") else None
        }
        return metadata
    else:
        print(f"Error: {response.status_code}")
        return None


# In[ ]:


# Ejemplo de uso:
if __name__ == "__main__":
    #x Variables
    #owner = "giosicolo"
    #repo = "api-backend-ecokit"

    #Por parametro
    owner = input("Ingrese el propietario del repositorio (owner): ")
    repo = input("Ingrese el nombre del repositorio (repo): ")

    meta = getMetadata(owner, repo)
    if meta:
        print("\n Los metadatos del repositorio son: \n")
        for key, value in meta.items():

            print(f"{key}: {value}")


# In[15]:


def getAllIssues(owner, repo, state):

    all_issues = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"

        params = {
            "state": state,
            "per_page": 100,
            "page": page
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        issues = response.json()
        # si no quedan issues por tomar
        if not issues:
            break

        all_issues.extend(issues)
        #Cambio de pagina - Git Hub te deja tomar hasta 100 por pagina
        page += 1

    return all_issues


# In[19]:


def printIssue(issue):
    print(f"{'='*80}")
    print(f"Issue #{issue.get('number')}: {issue.get('title')}")
    print(f"Estado: {issue.get('state')}")
    print(f"URL: {issue.get('html_url')}")
    print(f"Usuario: {issue.get('user', {}).get('login')}")
    print(f"Etiquetas: {[label['name'] for label in issue.get('labels', [])]}")
    print(f"Asignado a: {issue.get('assignee', {}).get('login') if issue.get('assignee') else 'Nadie'}")
    print(f"Participantes: {issue.get('comments')} comentario(s)")
    print(f"Fecha de creación: {issue.get('created_at')}")
    print(f"Última actualización: {issue.get('updated_at')}")
    print(f"Cerrado en: {issue.get('closed_at')}")
    print(f"Milestone: {issue.get('milestone', {}).get('title') if issue.get('milestone') else 'Ninguno'}")
    print(f"Es pull request: {'Sí' if 'pull_request' in issue else 'No'}")
    print("\nDescripción:")
    print(issue.get('body') if issue.get('body') else "(Sin descripción)")
    print(f"{'='*80}\n")


# In[20]:


#owner = "giosicolo"
#repo = "api-backend-ecokit"

#Por parametro
owner = input("Ingrese el propietario del repositorio (owner): ")
repo = input("Ingrese el nombre del repositorio (repo): ")

issues = getAllIssues(owner, repo, state="open")
if issues:
    for issue in issues:
        if "pull_request" not in issue:
            printIssue(issue)




# In[ ]:




