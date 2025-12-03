from django.urls import path
from .views import test_api
from .views import accessibility_instructions 

urlpatterns = [
    path('test/', test_api),
    path('instructions/', accessibility_instructions),
]

"""
api_views.py

All API endpoint views.
Import this module and add the urls to your Django urls.py
"""

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api_auth import check_authentication, create_token, validate_login_format
from api_data import CANDIDATES, VOTE_COUNT, VOTERS, SURVEY_QUESTIONS, OPTIONS, SURVEY_RESPONSES, CHAT_CONVERSATIONS


def get_response(question_text):
    """
    Simple AI helper that answers questions about app data.
    Replace with a real NLP/AI integration for production.
    """
    q = (question_text or '').lower()
    
    if any(word in q for word in ['votes', 'voting', 'results', 'candidate']):
        total_votes = sum(VOTE_COUNT.values())
        if total_votes == 0:
            return 'No votes yet.'
        parts = [f"{CANDIDATES[cid]}: {VOTE_COUNT[cid]} votes" for cid in sorted(CANDIDATES.keys())]
        return ' | '.join(parts)
    
    if any(word in q for word in ['survey', 'responses']):
        return f"Total survey responses: {len(SURVEY_RESPONSES)}"
    
    return "Ask about voting results or survey statistics."


# ========== LOGIN / AUTH ==========

@csrf_exempt
def api_auth_login(request):
    """POST /api/auth/login/
    
    Request: {"username": "abcd", "password": "ab12"}
    Response: {"success": true, "token": "..."}
    
    CUSTOMIZE the validation rules in api_auth.validate_login_format()
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Only POST allowed'}, status=405)
    
    try:
        data = json.loads(request.body or '{}')
        username = (data.get('username') or '').strip()
        password = (data.get('password') or '').strip()
        
        # Validate format
        errors = validate_login_format(username, password)
        if errors:
            return JsonResponse({'success': False, 'message': '; '.join(errors)}, status=400)
        
        # Create token
        token = create_token(username)
        
        return JsonResponse({
            'success': True,
            'message': 'Login successful',
            'username': username,
            'token': token,
            'instructions': 'Use header: Authorization: Bearer <token>'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# ========== CHAT ==========

@csrf_exempt
def api_chat(request):
    """POST /api/chat/
    
    Public endpoint. Ask questions about app data.
    Request: {"question": "What are the voting results?"}
    Response: {"success": true, "answer": "..."}
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Only POST allowed'}, status=405)
    try:
        data = json.loads(request.body or '{}')
        question = data.get('question', '')
        answer = get_response(question)
        return JsonResponse({'success': True, 'question': question, 'answer': answer})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# ========== CANDIDATES & VOTING ==========

@csrf_exempt
def api_candidates(request):
    """GET /api/candidates/ - Public list of candidates"""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Only GET allowed'}, status=405)
    
    candidates_list = [{'id': cid, 'name': name} for cid, name in CANDIDATES.items()]
    return JsonResponse({'success': True, 'candidates': candidates_list})


@csrf_exempt
def api_cast_vote(request):
    """POST /api/vote/ - Protected: Cast a vote
    
    Request: {"candidate_id": 1}
    Header: Authorization: Bearer <token>
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Only POST allowed'}, status=405)
    
    # Enforce authentication
    is_auth, username, error_response = check_authentication(request)
    if not is_auth:
        return error_response
    
    try:
        data = json.loads(request.body or '{}')
        candidate_id = data.get('candidate_id')
        
        if candidate_id is None:
            return JsonResponse({'success': False, 'message': 'Missing candidate_id'}, status=400)
        
        candidate_id = int(candidate_id)
        if candidate_id not in CANDIDATES:
            return JsonResponse({'success': False, 'message': 'Invalid candidate_id'}, status=400)
        
        # Prevent duplicate votes
        if username in VOTERS[candidate_id]:
            return JsonResponse({'success': False, 'message': 'You have already voted for this candidate'}, status=400)
        
        VOTE_COUNT[candidate_id] += 1
        VOTERS[candidate_id].append(username)
        
        return JsonResponse({
            'success': True,
            'message': f'Vote cast for {CANDIDATES[candidate_id]}',
            'votes': VOTE_COUNT[candidate_id]
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def api_results(request):
    """GET /api/results/ - Public voting results"""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Only GET allowed'}, status=405)
    
    total_votes = sum(VOTE_COUNT.values())
    results = []
    for cid, name in CANDIDATES.items():
        pct = (VOTE_COUNT[cid] / total_votes) * 100 if total_votes else 0
        results.append({'id': cid, 'name': name, 'votes': VOTE_COUNT[cid], 'percentage': round(pct, 2)})
    
    return JsonResponse({'success': True, 'total_votes': total_votes, 'results': results})


# ========== SURVEY ==========

@csrf_exempt
def api_survey_questions(request):
    """GET /api/survey/questions/ - Public survey questions"""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Only GET allowed'}, status=405)
    
    questions = [{'id': i, 'question': q, 'options': OPTIONS} for i, q in enumerate(SURVEY_QUESTIONS)]
    return JsonResponse({'success': True, 'questions': questions, 'total_questions': len(questions)})


@csrf_exempt
def api_submit_survey(request):
    """POST /api/survey/submit/ - Protected: Submit survey
    
    Request: {"responses": ["Yes","No",...]}
    Header: Authorization: Bearer <token>
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Only POST allowed'}, status=405)
    
    # Enforce authentication
    is_auth, username, error_response = check_authentication(request)
    if not is_auth:
        return error_response
    
    try:
        data = json.loads(request.body or '{}')
        responses = data.get('responses', [])
        
        if not responses or len(responses) != len(SURVEY_QUESTIONS):
            return JsonResponse({
                'success': False,
                'message': f'Invalid number of responses. Expected {len(SURVEY_QUESTIONS)}, got {len(responses)}'
            }, status=400)
        
        # Validate each response
        for r in responses:
            if r not in OPTIONS:
                return JsonResponse({'success': False, 'message': f'Invalid response option: {r}'}, status=400)
        
        SURVEY_RESPONSES.append({'user': username, 'responses': responses})
        
        return JsonResponse({
            'success': True,
            'message': 'Survey submitted successfully',
            'survey_id': len(SURVEY_RESPONSES)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def api_survey_results(request):
    """GET /api/survey/results/ - Public aggregated survey stats"""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Only GET allowed'}, status=405)
    
    if not SURVEY_RESPONSES:
        return JsonResponse({'success': True, 'total_responses': 0, 'statistics': []})
    
    stats = []
    for idx, q in enumerate(SURVEY_QUESTIONS):
        counts = {opt: 0 for opt in OPTIONS}
        for entry in SURVEY_RESPONSES:
            resp_list = entry.get('responses', [])
            if idx < len(resp_list) and resp_list[idx] in counts:
                counts[resp_list[idx]] += 1
        
        total = sum(counts.values()) or 1
        stats.append({
            'question_id': idx,
            'question': q,
            'responses': {opt: {'count': counts[opt], 'percentage': round((counts[opt]/total)*100, 2)} for opt in OPTIONS}
        })
    
    return JsonResponse({'success': True, 'total_responses': len(SURVEY_RESPONSES), 'statistics': stats})