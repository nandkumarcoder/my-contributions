import os
import subprocess
import random
import shutil
from datetime import datetime, timedelta

def run_git_command(args, env=None):
    if args[0] == 'git':
        args[0] = r"C:\Program Files\Git\cmd\git.exe"
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    return result

def main():
    print("Re-initializing contributions to exactly 25 commits over the last year...")
    
    # 1. Reset HEAD to start a fresh branch history
    run_git_command(['git', 'update-ref', '-d', 'HEAD'])
    
    filename = 'contribution_history.txt'
    if os.path.exists(filename):
        os.remove(filename)
        
    # 2. Pick 25 unique random dates within the last 365 days
    today = datetime.now()
    dates = []
    
    while len(dates) < 25:
        random_days_ago = random.randint(1, 365)
        commit_date = today - timedelta(days=random_days_ago)
        # Avoid duplicate days
        date_str = commit_date.strftime("%Y-%m-%d")
        if date_str not in [d.strftime("%Y-%m-%d") for d in dates]:
            dates.append(commit_date)
            
    # Sort dates chronologically
    dates.sort()
    
    # 3. Create the 25 commits
    for idx, commit_date in enumerate(dates):
        # Format timestamp with random work hours
        timestamp = commit_date.replace(
            hour=random.randint(9, 17),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        ).isoformat()
        
        with open(filename, 'a') as f:
            f.write(f"Contribution #{idx+1} - Date: {timestamp}\n")
            
        env = os.environ.copy()
        env['GIT_AUTHOR_DATE'] = timestamp
        env['GIT_COMMITTER_DATE'] = timestamp
        
        run_git_command(['git', 'add', filename])
        commit_msg = f"Feature deployment revision #{idx+1}"
        run_git_command(['git', 'commit', '-m', commit_msg], env=env)
        
    print(f"Successfully generated exactly {len(dates)} commits spread over the last year!")

if __name__ == '__main__':
    main()
