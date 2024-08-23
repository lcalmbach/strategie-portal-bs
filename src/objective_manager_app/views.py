from enum import Enum
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy   
from .models import BusinessObject, PlanRecord, Massnahme, Ziel, Handlungsfeld, Person, Organisation, MassnahmeOrganisation
from .forms import PlanRecordMVForm, PlanRecordSPForm, PlanRecordFGSForm, PersonForm, OrganisationForm,ZielForm,HandlungsfeldForm, MassnahmeForm, MassnahmeOrganisationForm
from django.contrib.auth.mixins import LoginRequiredMixin
import plotly.graph_objs as go
from .templatetags.custom_filters import is_in_group
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from datetime import datetime

from .planung import Planung

class ObjectType(Enum):
    HANDLUNGSFELD = 2
    ZIEL = 3
    MASSNAHME = 4
    PLAN_RECORD = 5

def is_in_group_decorator(group_name):
    return user_passes_test(lambda u: is_in_group(u, group_name))


def handlungsfelder_list(request):
    handlungsfelder = Handlungsfeld.objects.all()
    context = {
        'handlungsfelder': handlungsfelder,
    }
    return render(
        request,
        "objective_manager_app/handlungsfelder_list.html",
        context,
    )


def ziele_list(request):
    ziele = Ziel.objects.all()
    context = {
        'ziele': ziele,
    }
    return render(request, "objective_manager_app/ziele_list.html", context)


def massnahmen_list(request):
    massnahmen = Massnahme.objects.all()
    # Get filter values from the request
    filter_ziel = request.GET.get('filterZiel', '')
    filter_kuerzel = request.GET.get('filterKuerzel', '')
    filter_titel = request.GET.get('filterTitel', '')
    filter_beschreibung = request.GET.get('filterBeschreibung', '')

    # Apply additional filters if provided
    if filter_ziel:
        massnahmen = massnahmen.filter(vorgaenger__kuerzel__icontains=filter_ziel) | massnahmen.filter(vorgaenger__titel__icontains=filter_ziel)
    
    if filter_kuerzel:
        massnahmen = massnahmen.filter(kuerzel__icontains=filter_kuerzel)
    
    if filter_titel:
        massnahmen = massnahmen.filter(titel__icontains=filter_titel)
    
    if filter_beschreibung:
        massnahmen = massnahmen.filter(text__icontains=filter_beschreibung)

    # Prepare the context with the filtered queryset
    context = {
        'massnahmen': massnahmen,
        'filterZiel': filter_ziel,
        'filterKuerzel': filter_kuerzel,
        'filterTitel': filter_titel,
        'filterBeschreibung': filter_beschreibung,
    }

    return render(
        request,
        "objective_manager_app/massnahmen_list.html",
        context,
    )

def personen_list(request):
    personen = Person.objects.all()
    
    context = {
        'personen': personen,
    }
    return render(request, "objective_manager_app/personen_list.html", context)


def organisationen_list(request):
    organisationen = Organisation.objects.all()
    strategie_auswahl_id = request.session.get('strategie_id', None)
    context = {
        'organisationen': organisationen,
    }
    return render(request, "objective_manager_app/organisationen_list.html", context)


def plan_records_list(request):
    plan_records = PlanRecord.objects.all()
    departement_choices = Organisation.objects.values_list('departement_kuerzel', flat=True).distinct().order_by('departement_kuerzel').order_by('departement_kuerzel')

    if request.method == "POST":
        pass
        # if planung.run():
        #     messages.success(request, "Die Planung wurde erfolgreich erstellt.")
        # else:   
        #    messages.warning(request, "Bei der Erstellung der Planung ist ein Fehler aufgetreten.")
    else:
        # Filter basierend auf GET-Parameter
        jahr = request.GET.get('jahr')
        if jahr:
            plan_records = plan_records.filter(jahr__icontains=jahr)
        
        organisation = request.GET.get('organisation')
        if organisation:
            plan_records = plan_records.filter(bereich__icontains=organisation)
        
        departement = request.GET.get('departement')
        if departement:
            plan_records = plan_records.filter(departement__kuerzel__icontains=departement)
        
        massnahme = request.GET.get('massnahme')
        if massnahme:
            plan_records = plan_records.filter(massnahme__titel__icontains=massnahme)
        
    context = {
        'plan_records': plan_records,
        'departement_choices': departement_choices,
    }  
    return render(
        request,
        "objective_manager_app/home.html",
        context,
    )


# Detail Views
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
    massnahmen = BusinessObject.objects.filter(typ_id=ObjectType.MASSNAHME.value, vorgaenger=ziel)
    context = {
        'ziel': ziel,
        'massnahmen': massnahmen,
    }

    return render(request, 'objective_manager_app/ziel_detail.html', context)


def massnahme_detail(request, pk):
    massnahme = get_object_or_404(BusinessObject, pk=pk)
    massnahme_orgs = MassnahmeOrganisation.objects.filter(massnahme=massnahme)
    context = {
        'massnahme': massnahme,
        'massnahme_orgs': massnahme_orgs,
    }
    return render(
        request,
        "objective_manager_app/massnahme_detail.html",
        context,
    )


def plan_record_detail(request, pk):
    plan_record = get_object_or_404(PlanRecord, pk=pk)
    plan_records = PlanRecord.objects.filter(objekt=plan_record)
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
        'plan_records': plan_records,
    }
    return render(request, 'dein_template_name.html', context)

    return render(
        request,
        "objective_manager_app/plan_record_detail.html",
        {"plan_records": plan_records, "plot_div": plot_div, 'massnahme': massnahme},
    )


def home(request, pk):
    if request.method == "POST":
        request.session['strategie_id'] = request.POST.get('strategie_auswahl')
    else:
        request.session['strategie_id'] = pk
    
    return render(
        request,
        "objective_manager_app/home.html",
    )


def home_detail(request):
    if request.method == "POST":
        request.session['strategie_id'] = request.POST.get('strategie_auswahl')
    else:
        if not 'strategie_id' in request.session:
            request.session['strategie_id'] = 2
    
    return render(
        request,
        "objective_manager_app/home.html",
    )


def admin_detail(request):
    themes = BusinessObject.themen.all()
    selected_theme = None

    if request.method == "POST":
        selected_theme_id = request.POST.get("theme")
        request.session["selected_theme_id"] = selected_theme_id
        selected_theme = BusinessObject.themen.get(id=selected_theme_id)
    return render(
        request,
        "objective_manager_app/home.html",
        {"themes": themes, "selected_theme": selected_theme},
    )

@method_decorator(is_in_group_decorator('admins'), name='dispatch')
class HandlungsfeldEditView(UpdateView):
    model = Handlungsfeld
    form_class = HandlungsfeldForm
    template_name = 'objective_manager_app/handlungsfeld_edit.html'  # Path to your template

    def get_success_url(self):
        # Redirect to the detail page after a successful form submission
        return reverse_lazy('handlungsfeld_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed
        obj = form.save(commit=False)
        obj.erstellt_von = self.request.user  # Ensure the correct user is set
        obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ziel'] = self.object.vorgaenger 
        return context


@method_decorator(is_in_group_decorator('admins'), name='dispatch')
class ZielEditView(UpdateView):
    model = Ziel
    form_class = ZielForm
    template_name = 'objective_manager_app/ziel_edit.html'  # Path to your template

    def get_success_url(self):
        # Redirect to the detail page after a successful form submission
        return reverse_lazy('ziel_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed
        obj = form.save(commit=False)
        obj.erstellt_von = self.request.user  # Ensure the correct user is set
        obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['handlungsfeld'] = self.object.vorgaenger  # Add the vorgaenger (handlungsfeld) to the context
        return context


@method_decorator(is_in_group_decorator('admins'), name='dispatch')
class MassnahmeEditView(UpdateView):
    model = Massnahme
    form_class = MassnahmeForm
    template_name = 'objective_manager_app/massnahme_edit.html'  # Path to your template

    def get_success_url(self):
        # Redirect to the detail page after a successful form submission
        return reverse_lazy('massnahme_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed
        obj = form.save(commit=False)
        obj.erstellt_von = self.request.user  # Ensure the correct user is set
        obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ziel'] = self.object.vorgaenger  
        return context


class PlanRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = PlanRecord
    template_name = "objective_manager_app/plan_record_edit.html"
    context_object_name = 'plan_record'
    success_url = reverse_lazy('home')  # Adjust this as needed

    def get_form_class(self):
        # Check user's group and return the corresponding form class
        user = self.request.user
        if user.groups.filter(name='mv').exists():
            return PlanRecordMVForm
        elif user.groups.filter(name='sp').exists():
            return PlanRecordSPForm
        elif user.groups.filter(name='fgs').exists():
            return PlanRecordFGSForm
        else:
            pass # raise PermissionDenied("You are not authorized to edit this record.")  # Handle unauthorized access

    def form_valid(self, form):
        plan_record = form.save(commit=False)
        plan_record.erstellt_von = self.request.user
        plan_record.save()
        return redirect('home')



@is_in_group_decorator('admins')
def person_edit(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect("personen_list")
    else:
        form = PersonForm(instance=person)
    context = {
        "form": form,
    }
    return render(request, "objective_manager_app/person_edit.html", context)


@is_in_group_decorator('admins')
def organisation_edit(request, pk):
    organisation = get_object_or_404(Organisation, pk=pk)
    if request.method == "POST":
        form = OrganisationForm(request.POST, instance=organisation)
        if form.is_valid():
            form.save()
            return redirect("organisationen_list")
    else:
        form = OrganisationForm(instance=organisation)
    context = {
        "form": form,
    }
    return render(request, "objective_manager_app/organisation_edit.html", context)

# -----------------------------------
# delete views
#------------------------------------

def person_delete(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == "POST":
        person.delete()
        return redirect('personen_list')
    
def organisation_delete(request, pk):
    organisation = get_object_or_404(Organisation, pk=pk)
    if request.method == "POST":
        organisation.delete()
        return redirect('organisationen_list')

def handlungsfeld_delete(request, pk):
    handlungsfeld = get_object_or_404(Handlungsfeld, pk=pk)
    if request.method == "POST":
        handlungsfeld.delete()
        return redirect('handlungsfelder_list')

# -----------------------------------
# add views
#------------------------------------
    
class OrganizationCreateView(CreateView):
    model = Organisation
    form_class = OrganisationForm
    template_name = 'objective_manager_app/organisation_edit.html'
    success_url = reverse_lazy('organisationen_list')  

class MassnahmeCreateView(CreateView):
    model = Massnahme
    form_class = MassnahmeForm
    template_name = 'objective_manager_app/massnahme_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ziel = Ziel.objects.get(pk=self.kwargs['ziel_id'])
        return context
    
    def form_valid(self, form):
        # Assign additional fields before saving the object
        obj = form.save(commit=False)
        obj.erstellt_von = self.request.user
        obj.typ_id = ObjectType.MASSNAHME.value  

        # Get the ziel_id from the URL kwargs and set it as the vorgaenger
        ziel_id = self.kwargs['ziel_id']
        obj.vorgaenger = get_object_or_404(BusinessObject, pk=ziel_id)

        messages.success(self.request, "Die Massnahme wurde erfolgreich in der Datenbank gespeichert.")
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the edit page for the newly created Massnahme
        return reverse('massnahme_edit', kwargs={'pk': self.object.pk})
    
class MassnahmeOrgCreateView(CreateView):
    model = MassnahmeOrganisation
    form_class = MassnahmeOrganisationForm
    template_name = 'objective_manager_app/massnahme_organisation_edit.html'

    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill form fields with initial values
        massnahme_id = self.kwargs.get('massnahme_id')
        initial['massnahme'] = massnahme_id  # Assuming 'massnahme' is the field name in the form
        return initial

    def form_valid(self, form):
        # Assign additional fields before saving the object
        obj = form.save(commit=False)
        obj.erstellt_von = self.request.user
        massnahme_id = self.kwargs.get('massnahme_id')
        obj.massnahme_id = massnahme_id  # Set massnahme_id if the field is in the model
        messages.success(self.request, "Die Zuweisung wurde erfolgreich in der Datenbank gespeichert.")
        obj.save()
        return super().form_valid(form)

    def get_strategie(self, massnahme_id):
        # Fetch the related strategie object
        massnahme = get_object_or_404(Massnahme, pk=massnahme_id)
        return massnahme.strategie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        massnahme = Massnahme.objects.get(pk=self.kwargs['massnahme_id'])
        return context

    def get_success_url(self):
        # Reverse the URL to the edit page for the newly created MassnahmeOrganisation
        return reverse('massnahme_detail', kwargs={'pk': self.object.massnahme.pk})


class MassnahmeOrganisationUpdateView(UpdateView):
    model = MassnahmeOrganisation
    fields = ['massnahme', 'organisation', 'person', 'bemerkungen', 'rolle']
    template_name = 'objective_manager_app/massnahme_organisation_edit.html'
    context_object_name = 'massnahmeorganisation'
    success_url = reverse_lazy('massnahmeorganisation_list')  # Replace with your success URL, like the list or detail view
    

class ZielCreateView(CreateView):
    model = BusinessObject
    form_class = ZielForm
    template_name = 'objective_manager_app/ziel_edit.html'

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        handlungsfeld = Handlungsfeld.objects.get(pk=self.kwargs['handlungsfeld_id'])
        return context
    
    def form_valid(self, form):
        # Assign additional fields before saving the object
        obj = form.save(commit=False)
        obj.erstellt_von = self.request.user
        obj.typ_id = ObjectType.ZIEL.value  
        handlungsfeld_id = self.kwargs['handlungsfeld_id']
        obj.vorgaenger = get_object_or_404(BusinessObject, pk=handlungsfeld_id)
        messages.success(self.request, "Das Ziel wurde erfolgreich in der Datenbank gespeichert.")
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Reverse the URL to the edit page for the newly created Ziel
        return reverse('ziel_edit', kwargs={'pk': self.object.pk})


class HandlungsfeldCreateView(LoginRequiredMixin, CreateView):
    model = BusinessObject
    form_class = HandlungsfeldForm
    template_name = 'objective_manager_app/handlungsfeld_edit.html'  # Update with your template path
    success_url = reverse_lazy('handlungsfelder_list')  # Replace with your actual success URL

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def form_valid(self, form):
        # Assign additional fields before saving the object
        obj = form.save(commit=False)
        obj.erstellt_von = self.request.user
        obj.typ_id = ObjectType.HANDLUNGSFELD.value  
        obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Add additional context data if necessary
        context = super().get_context_data(**kwargs)
        return context

class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'objective_manager_app/person_edit.html'
    success_url = reverse_lazy('personen_list') 

class PlanRecordCreateView(CreateView):
    model = PlanRecord
    form_class = PlanRecordMVForm
    template_name = 'objective_manager_app/plan_record_edit.html'
    success_url = reverse_lazy('home') 

