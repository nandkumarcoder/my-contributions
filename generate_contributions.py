import os
import subprocess
import random
from datetime import datetime, timedelta

def run_git_command(args, env=None):
    if args[0] == 'git':
        args[0] = r"C:\Program Files\Git\cmd\git.exe"
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    return result

def main():
    print("Initializing contribution generator...")
    
    # Initialize Git if not already done
    if not os.path.exists('.git'):
        run_git_command(['git', 'init'])
        run_git_command(['git', 'branch', '-M', 'main'])
    
    # Target file to modify
    filename = 'contribution_history.txt'
    
    # Generate commits for the last 90 days
    today = datetime.now()
    start_date = today - timedelta(days=90)
    
    total_commits = 0
    
    # Iterate through each day
    current_date = start_date
    while current_date <= today:
        # Avoid committing every single day to make it look natural (e.g., 70% chance of committing)
        if random.random() < 0.7:
            # Generate between 1 and 3 commits for this day
            num_commits = random.randint(1, 3)
            for i in range(num_commits):
                # Format timestamp
                timestamp = current_date.replace(
                    hour=random.randint(9, 18),
                    minute=random.randint(0, 59),
                    second=random.randint(0, 59)
                ).isoformat()
                
                # Write to dummy file
                with open(filename, 'a') as f:
                    f.write(f"Commit date: {timestamp}\n")
                
                # Setup custom environment variables for git commit date
                env = os.environ.copy()
                env['GIT_AUTHOR_DATE'] = timestamp
                env['GIT_COMMITTER_DATE'] = timestamp
                
                # Stage and commit
                run_git_command(['git', 'add', filename])
                commit_msg = f"Update contribution history log - {timestamp}"
                run_git_command(['git', 'commit', '-m', commit_msg], env=env)
                
                total_commits += 1
                
        current_date += timedelta(days=1)
        
    print(f"Generated {total_commits} commits successfully over the last 90 days!")
    print("Next steps:")
    print("1. Set your remote origin: git remote add origin <your-repo-url>")
    print("2. Push to GitHub: git push -u origin main")

if __name__ == '__main__':
    main()
