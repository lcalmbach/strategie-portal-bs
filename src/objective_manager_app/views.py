from django.shortcuts import render, get_object_or_404, redirect
from .models import BusinessObject, PlanRecord, Massnahme, Ziel, Handlungsfeld
from .forms import BusinessObjectForm, PlanRecordForm
import plotly.graph_objs as go

# List Views
def themen_list(request):
    themen = BusinessObject.themen.all()
    return render(request, "objective_manager_app/themen_list.html", {"themen": themen})


def handlungsfelder_list(request):
    handlungsfelder = BusinessObject.handlungsfelder.all()
    return render(
        request,
        "objective_manager_app/handlungsfelder_list.html",
        {"handlungsfelder": handlungsfelder},
    )


def ziele_list(request):
    ziele = BusinessObject.ziele.all()
    return render(request, "objective_manager_app/ziele_list.html", {"ziele": ziele})


def massnahmen_list(request):
    massnahmen = BusinessObject.massnahmen.all()
    return render(
        request,
        "objective_manager_app/massnahmen_list.html",
        {"massnahmen": massnahmen},
    )


def plan_records_list(request):
    plan_records = PlanRecord.objects.all()
    
    # Filter basierend auf GET-Parameter
    jahr = request.GET.get('jahr')
    print(jahr)
    if jahr:
        plan_records = plan_records.filter(jahr__icontains=jahr)
    
    organisation = request.GET.get('organisation')
    if organisation:
        plan_records = plan_records.filter(organisation__kuerzel__icontains=organisation)
    
    massnahme = request.GET.get('massnahme')
    if massnahme:
        plan_records = plan_records.filter(objekt__titel__icontains=massnahme)
    
    erfuellung_soll = request.GET.get('erfuellung_soll')
    if erfuellung_soll:
        plan_records = plan_records.filter(soll_wert_erreicht_pzt__icontains=erfuellung_soll)
    
    erfuellung_ist = request.GET.get('erfuellung_ist')
    if erfuellung_ist:
        plan_records = plan_records.filter(ist_wert_erreicht_pzt__icontains=erfuellung_ist)
    
    aufwand_soll = request.GET.get('aufwand_soll')
    if aufwand_soll:
        plan_records = plan_records.filter(soll_wert_erreicht_pzt__icontains=aufwand_soll)
    
    aufwand_ist = request.GET.get('aufwand_ist')
    if aufwand_ist:
        plan_records = plan_records.filter(ist_wert_erreicht_pzt__icontains=aufwand_ist)
    
    return render(
        request,
        "objective_manager_app/plan_records_list.html",
        {"plan_records": plan_records},
    )


# Detail Views
def thema_detail(request, pk):
    print(pk)
    thema = get_object_or_404(BusinessObject.themen, pk=pk)
    return render(request, "objective_manager_app/thema_detail.html", {"thema": thema})


def handlungsfeld_detail(request, pk):
    handlungsfeld = get_object_or_404(Handlungsfeld, pk=pk)
    
    ziele = BusinessObject.objects.filter(typ_id=3, vorgaenger=handlungsfeld)
    massnahmen = BusinessObject.objects.filter(typ_id=4, vorgaenger__in=ziele)
    # print(massnahmen)
    context = {
        'handlungsfeld': handlungsfeld,
        'ziele': ziele,
        'massnahmen': massnahmen,
    }
    return render(request, 'objective_manager_app/handlungsfeld_detail.html', context)


def ziel_detail(request, pk):
    ziel = get_object_or_404(BusinessObject.ziele, pk=pk)
    massnahmen = BusinessObject.objects.filter(typ_id=4, vorgaenger=ziel)
    context = {
        'ziel': ziel,
        'massnahmen': massnahmen,
    }

    return render(request, 'objective_manager_app/ziel_detail.html', context)


def massnahme_detail(request, pk):
    massnahme = get_object_or_404(BusinessObject, pk=pk)

    return render(
        request,
        "objective_manager_app/massnahme_detail.html",
        {"massnahme": massnahme},
    )


def plan_record_detail(request, pk):
    plan_record = get_object_or_404(PlanRecord, pk=pk)
    plan_records = PlanRecord.objects.filter(objekt=plan_record.objekt)
    massnahme = Massnahme.objects.get(pk=plan_record.objekt.pk)
    # Prepare data for the plot
    years = [pr.jahr for pr in plan_records]
    soll_wert_erreicht_pzt = [pr.soll_wert_erreicht_pzt for pr in plan_records]
    ist_wert_erreicht_pzt = [pr.ist_wert_erreicht_pzt for pr in plan_records]

    soll_aufwand_personen_tage = [pr.aufwand_personen_tage_plan for pr in plan_records]
    ist_aufwand_personen_tage = [pr.aufwand_personen_tage_ist for pr in plan_records]
    personen_tage_pzt = [(ist / soll) * 100 if soll else 0 for soll, ist in zip(soll_aufwand_personen_tage, ist_aufwand_personen_tage)]

    soll_aufwand_tsd_chf = [pr.aufwand_tsd_chf_plan for pr in plan_records]
    ist_aufwand_tsd_chf = [pr.aufwand_tsd_chf_ist for pr in plan_records]
    aufwand_tsd_chf_pzt = [(ist / soll) * 100 if soll else 0 for soll, ist in zip(soll_aufwand_tsd_chf, ist_aufwand_tsd_chf)]

    # Create the plotly figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=years, y=soll_wert_erreicht_pzt, mode='lines+markers', name='Soll Erfüllungsgrad'))
    fig.add_trace(go.Scatter(x=years, y=ist_wert_erreicht_pzt, mode='lines+markers', name='Ist Erfüllungsgrad'))
    fig.add_trace(go.Scatter(x=years, y=personen_tage_pzt, mode='lines+markers', name='Personentage Erfüllungsgrad'))
    fig.add_trace(go.Scatter(x=years, y=aufwand_tsd_chf_pzt, mode='lines+markers', name='Aufwand Erfüllungsgrad'))

    plot_div = fig.to_html(full_html=False)

    
    context = {
        'plan_records': plan_records
    }
    return render(request, 'dein_template_name.html', context)

    return render(
        request,
        "objective_manager_app/plan_record_detail.html",
        {"plan_records": plan_records, "plot_div": plot_div, 'massnahme': massnahme},
    )


def home_detail(request):
    themes = BusinessObject.themen.all()
    selected_theme = None

    if request.method == "POST":
        print("POST Data:", request.POST)
        selected_theme_id = request.POST.get("theme")
        print(selected_theme_id)
        request.session["selected_theme_id"] = selected_theme_id
        selected_theme = BusinessObject.themen.get(id=selected_theme_id)
    return render(
        request,
        "objective_manager_app/home.html",
        {"themes": themes, "selected_theme": selected_theme},
    )


def handlungsfeld_edit(request, pk):
    handlungsfeld = get_object_or_404(BusinessObject.handlungsfelder, pk=pk)
    if request.method == "POST":
        form = BusinessObjectForm(request.POST, instance=handlungsfeld)
        if form.is_valid():
            form.save()
            return redirect("handlungsfeld_detail", pk=handlungsfeld.pk)
    else:
        form = BusinessObjectForm(instance=handlungsfeld)
    return render(
        request, "objective_manager_app/handlungsfeld_edit.html", {"form": form}
    )


def ziel_edit(request, pk):
    ziel = get_object_or_404(BusinessObject.ziele, pk=pk)
    if request.method == "POST":
        form = BusinessObjectForm(request.POST, instance=ziel)
        if form.is_valid():
            form.save()
            return redirect("ziel_detail", pk=ziel.pk)
    else:
        form = BusinessObjectForm(instance=ziel)
    return render(request, "objective_manager_app/ziel_edit.html", {"form": form})


def massnahme_edit(request, pk):
    massnahme = get_object_or_404(BusinessObject.massnahmen, pk=pk)
    if request.method == "POST":
        form = BusinessObjectForm(request.POST, instance=massnahme)
        if form.is_valid():
            form.save()
            return redirect("massnahme_detail", pk=massnahme.pk)
    else:
        form = BusinessObjectForm(instance=massnahme)
    return render(request, "objective_manager_app/massnahme_edit.html", {"form": form})


def plan_record_edit(request, pk):
    plan_record = get_object_or_404(PlanRecord, pk=pk)
    if request.method == "POST":
        form = PlanRecordForm(request.POST, instance=plan_record)
        if form.is_valid():
            form.save()
            return redirect("plan_record_detail", pk=plan_record.pk)
    else:
        form = PlanRecordForm(instance=plan_record)
    return render(request, "objective_manager_app/plan_record_edit.html", {"form": form})