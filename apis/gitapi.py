import requests

def extract_owner_repo(url):
    """
    GitHub repo URL se owner aur repo extraction
    Supports URLs with or without .git
    Example URL:
        https://github.com/username/repo.git
        https://github.com/username/repo
    Returns:
        owner (str), repo_name (str)
    """
    url_part=url.split("/")
    if len(url_part):
        if len(url_part) < 2:
            raise ValueError("Invalid GitHub repository URL")
    
    owner = url_part[-2]   # second last part
    repo_name = url_part[-1]  # last part

    return owner, repo_name



def fetch_repo_metadata(owner, repo):
    '''
    Fetches metadata of public repos and return as dictionary
    dict contains reponame, repo_url, desc, language, topic,
    stars, license, files name as string

    Returns:
        metadata (dict)
    '''
    header = {"Accept": "application/vnd.github.mercy-preview+json"}  #??

    repo_data_url = f"https://api.github.com/repos/{owner}/{repo}"  #api url for metadata 
    response = requests.get(repo_data_url, headers=header)    #api call to fetch metadata
    
    if response.status_code != 200:                      #ASK GPT
        raise Exception(f"Failed to fetch repo: {response.status_code}")
    repo_data = response.json()

    content_file_url=f"https://api.github.com/repos/{owner}/{repo}/contents"  #api url for file contents
    cont_response=requests.get(content_file_url,headers=header)

    files_list=[]    #list of content files

    if cont_response.status_code == 200:  #extraction of file names of the project repo
        for f in cont_response.json():
            files_list.append(f["name"])

    #creating meta data for gemini
    metadata={
        "repo_name": repo_data.get('name'),
        "repo_url": repo_data.get("html_url"),
        "repo_description": repo_data.get("description"),
        "language": repo_data.get("language"),
        "topics": ", ".join(repo_data.get("topics", [])),
        "stars": repo_data.get("stargazers_count", 0),
        "license_name": repo_data.get("license", {}).get("name") if repo_data.get("license") else "Not specified",
        "files":", ".join(files_list)
    }

    return metadata







