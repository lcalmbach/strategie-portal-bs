# Straplaco

Straplaco is an application designed to support the process of strategic planning and controlling. It assumes the common hierarchical structure of Handlungsfeld (Action Field) > Ziel (Objective) > Massnahme (Measure) and allows users to manage the yearly planning of the required activities.

## Features

- **Hierarchical Management**: Manage strategic plans through a structured hierarchy of action fields, objectives, and measures.
- **Yearly Planning**: Facilitate the yearly planning process by organizing activities within the given hierarchical structure.
- **Progress Tracking**: Track the progress of each objective and measure through planned versus actual completion rates.
- **Financial and Labor Effort Management**: Monitor financial and labor efforts in terms of planned and actual values, allowing for effective resource management.
- **Visual Representation**: Display data visually using Plotly charts for easy comparison of planned versus actual values over time.

## Models

### BusinessObject

The `BusinessObject` model serves as a base model for the hierarchical structure and includes common fields such as title, description, creation date, and more.

### Handlungsfeld (Action Field)

The `Handlungsfeld` model represents an action field within the strategic planning process.

### Ziel (Objective)

The `Ziel` model represents an objective associated with a specific action field.

### Massnahme (Measure)

The `Massnahme` model represents a measure associated with a specific objective.

### PlanRecord

The `PlanRecord` model tracks the planned and actual values for a specific objective or measure, including completion rates, financial effort, and labor effort.

## Views

### plan_record_detail

The `plan_record_detail` view displays the details of a specific `PlanRecord` along with a table and a Plotly chart for visual comparison of planned versus actual values.

## Templates

### plan_record_detail.html

This template extends the base layout and displays the details of a `PlanRecord`, including:

- A table with the planned and actual values for the selected year.
- A Plotly line chart that visualizes the planned versus actual completion rates over the years.

## Usage

1. **Install Dependencies**

   Ensure you have the required dependencies installed:

   ```bash
   pip install django plotly
