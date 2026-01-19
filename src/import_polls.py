import yaml
import json
from datetime import datetime

def import_polls(yaml_file='config/polls.yaml', output='polls_data.json'):
    with open(yaml_file) as f:
        config = yaml.safe_load(f)
    
    polls = {}
    responses = {}
    
    for pid, data in config.get('polls', {}).items():
        polls[pid] = {
            'id': pid,
            'title': data.get('title', pid),
            'question': data.get('question', ''),
            'options': data.get('options', []),
            'created': datetime.now().isoformat(),
            'active': True
        }
        responses[pid] = []
        print(f"✓ {pid} - {data.get('title')}")
    
    with open(output, 'w') as f:
        json.dump({'polls': polls, 'responses': responses}, f, indent=2)
    
    print(f"\n✅ {len(polls)} polls created")

if __name__ == "__main__":
    import_polls()
