from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mainapp.models import ConceptTag, Topic

@login_required
def knowledge_graph_view(request):
    """
    Renders the D3.js Knowledge Graph container.
    """
    return render(request, 'mainapp/knowledge_graph.html')

@login_required
def knowledge_graph_data(request):
    """
    API endpoint returning JSON for D3 force-directed graph.
    Nodes: Topics and ConceptTags.
    Links: Topic->ConceptTag associations and Topic->ParentTopic.
    """
    from mainapp.models import Topic, ConceptTag
    
    nodes = []
    links = []
    
    # Track node IDs to avoid duplicates
    node_set = set()
    
    topics = Topic.objects.all().prefetch_related('study_materials__concept_tags')
    
    for t in topics:
        if f"topic_{t.id}" not in node_set:
            nodes.append({
                "id": f"topic_{t.id}",
                "name": t.name,
                "group": 1,  # 1 for Topics
                "val": 10
            })
            node_set.add(f"topic_{t.id}")
        
        # Link to parent topic simulating hierarchical dependency
        if t.parent_topic:
            links.append({
                "source": f"topic_{t.id}",
                "target": f"topic_{t.parent_topic.id}",
                "value": 2
            })
            
        # Link to concepts via study materials
        for material in t.study_materials.all():
            for tag in material.concept_tags.all():
                if f"concept_{tag.id}" not in node_set:
                    nodes.append({
                        "id": f"concept_{tag.id}",
                        "name": tag.name,
                        "group": 2, # 2 for Concepts
                        "val": 6
                    })
                    node_set.add(f"concept_{tag.id}")
                
                links.append({
                    "source": f"topic_{t.id}",
                    "target": f"concept_{tag.id}",
                    "value": 1
                })
                
    return JsonResponse({"nodes": nodes, "links": links})
