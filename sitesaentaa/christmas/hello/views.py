import random
from django.shortcuts import render, redirect
from .models import Participant
from .forms import ParticipantForm

def index(request):
    from datetime import datetime
    today = datetime.today()
    is_christmas = today.month == 12 and today.day == 25
    return render(request, 'index.html', {'is_christmas': is_christmas})

def generate_pairs(participants):
    """Generate secret santa pairs ensuring no one is their own santa."""
    names = [p.name for p in participants]
    if len(names) < 2:
        return None  # Not enough participants to generate pairs

    while True:
        random.shuffle(names)
        pairs = {names[i]: names[(i + 1) % len(names)] for i in range(len(names))}
        # Ensure no one is assigned to themselves
        if all(pairs[receiver] != receiver for receiver in pairs):
            return pairs

def secret_santa(request):
    if request.method == 'POST':
        if 'add_participant' in request.POST:
            form = ParticipantForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('secret_santa')
        elif 'generate' in request.POST:
            participants = Participant.objects.all()
            if len(participants) < 2:
                return render(request, 'secret_santa.html', {
                    'form': ParticipantForm(),
                    'participants': participants,
                    'error': 'Need at least two participants to generate pairs.'
                })

            pairs = generate_pairs(participants)
            if pairs is None:
                return render(request, 'secret_santa.html', {
                    'form': ParticipantForm(),
                    'participants': participants,
                    'error': 'Could not generate valid pairs. Try again.'
                })

            return render(request, 'secret_santa.html', {
                'form': ParticipantForm(),
                'participants': participants,
                'pairs': pairs
            })
        elif 'clear_list' in request.POST:
            Participant.objects.all().delete()
            return redirect('secret_santa')
    else:
        form = ParticipantForm()

    participants = Participant.objects.all()
    return render(request, 'secret_santa.html', {
        'form': form,
        'participants': participants
    })
