import yaml
import json
from datetime import datetime
from pathlib import Path
import sys

def import_polls(poll_file=None, output='polls_data.json'):
    polls = {}
    responses = {}
    
    if poll_file:
        files = [Path(poll_file)]
    else:
        files = list(Path('polls').rglob('*.yaml'))
    
    for file in files:
        with open(file) as f:
            config = yaml.safe_load(f)
        
        course = config.get('course', 'Unknown')
        week = config.get('week', '')
        
        for pid, data in config.get('polls', {}).items():
            full_id = f"{pid}_{course.split()[0].lower()}_{week}" if week else pid
            polls[full_id] = {
                'id': full_id,
                'title': data.get('title', pid),
                'question': data.get('question', ''),
                'options': data.get('options', []),
                'course': course,
                'week': week,
                'created': datetime.now().isoformat(),
                'active': True
            }
            responses[full_id] = []
            print(f"✓ {full_id} - {data.get('title')}")
    
    with open(output, 'w') as f:
        json.dump({'polls': polls, 'responses': responses}, f, indent=2)
    
    print(f"\n✅ {len(polls)} polls from {len(files)} files")

if __name__ == "__main__":
    import_polls(sys.argv[1] if len(sys.argv) > 1 else None)
