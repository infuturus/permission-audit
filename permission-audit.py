from github import Github
import csv
import os

# GitHub API Token (use environment variables for security)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set this in your environment
ORG_NAME = "your-org-name"  # Replace with your GitHub Organization name

# Initialize GitHub API client
g = Github(GITHUB_TOKEN)
org = g.get_organization(ORG_NAME)

# Output file
OUTPUT_CSV = "github_permissions_audit.csv"

def get_repo_permissions(repo):
    """Fetch user and team permissions for a given repository."""
    permissions = []

    # Get team permissions
    for team in repo.get_teams():
        permissions.append((ORG_NAME, repo.name, team.name, "N/A", team.permission))

    # Get individual user permissions
    for collab in repo.get_collaborators():
        permissions.append((ORG_NAME, repo.name, "N/A", collab.login, collab.permissions))

    return permissions

def audit_github_permissions():
    """Main function to list permissions across all repositories in the organization."""
    all_permissions = []
    
    for repo in org.get_repos():
        print(f"Processing repo: {repo.name}")
        all_permissions.extend(get_repo_permissions(repo))

    return all_permissions

def save_to_csv(data):
    """Save permission data to a CSV file."""
    with open(OUTPUT_CSV, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["OrgName", "RepoName", "GitHub Team", "UserName", "Permission"])
        writer.writerows(data)

    print(f"Permissions saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    permissions_data = audit_github_permissions()
    save_to_csv(permissions_data)
