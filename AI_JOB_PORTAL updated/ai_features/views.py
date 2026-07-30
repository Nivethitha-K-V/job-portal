from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import Resume, Skill
from jobs.models import Job
from .analyzer import analyze_resume, analyze_skill_gap
from .models import ResumeAnalysis, SkillGapReport


@login_required
def resume_analyzer(request):
    resume = Resume.objects.filter(user=request.user, is_active=True).first()
    result = None

    if request.method == 'POST':
        if not resume:
            messages.error(request, "Please upload a resume first.")
            return redirect('upload_resume')
        try:
            result = analyze_resume(resume.file)
        except Exception as exc:
            messages.error(request, f"Could not read the resume PDF: {exc}")
            return render(request, 'ai_features/resume_analyzer.html', {'resume': resume})

        resume.resume_score = result['score']
        resume.save(update_fields=['resume_score'])

        ResumeAnalysis.objects.create(
            user=request.user,
            resume=resume,
            score=result['score'],
            skills_detected=', '.join(result['skills_detected']),
            missing_skills=', '.join(result['missing_skills']),
            strengths='\n'.join(result['strengths']),
            weaknesses='\n'.join(result['weaknesses']),
            suggestions='\n'.join(result['suggestions']),
        )

    return render(request, 'ai_features/resume_analyzer.html', {
        'resume': resume,
        'result': result,
    })


@login_required
def skill_gap_analyzer(request):
    jobs = Job.objects.filter(is_active=True)
    selected_job = None
    result = None

    job_id = request.GET.get('job_id') or request.POST.get('job_id')
    if job_id:
        selected_job = get_object_or_404(Job, pk=job_id)
        candidate_skills = list(Skill.objects.filter(user=request.user).values_list('name', flat=True))
        result = analyze_skill_gap(candidate_skills, selected_job.skills_list)

        SkillGapReport.objects.create(
            user=request.user,
            job=selected_job,
            match_percentage=result['match_percentage'],
            missing_skills=', '.join(result['missing_skills']),
            recommended_courses='\n'.join(result['recommended_courses']),
        )

    return render(request, 'ai_features/skill_gap.html', {
        'jobs': jobs,
        'selected_job': selected_job,
        'result': result,
    })
