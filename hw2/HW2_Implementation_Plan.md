# HW2 Implementation Plan - Data and Visual Analytics

## Overview
This homework focuses on data visualization using D3.js. We'll implement Q2 (Force-directed graph), Q3 (Line Charts), Q4 (Interactive Visualization), and Q5 (Choropleth map), skipping Q1 (Tableau).

## Q2: Force-directed Graph Layout [15 points]

### Goal
Create a network graph showing relationships between games in D3 with interactive features like pinning nodes.

### Technology Requirements
- D3 Version 5 (provided in lib folder)
- Chrome v131.0.0 or higher
- Python HTTP server for local testing
- Dataset: board_games.csv (provided)

### Implementation Plan

#### 1. Node Labels [2 points]
- **Task**: Add node labels at top right of each node in bold
- **Requirements**:
  - Show node name (source) at top right
  - Labels must move with dragged nodes
  - Use bold text

#### 2. Edge Styling [3 points]
- **Task**: Style edges based on "value" field
- **Requirements**:
  - Value = 0 (similar): gray, thick, solid line
  - Value = 1 (not similar): green, thin, dashed line

#### 3. Node Scaling [3 points]
##### 3a. Radius Scaling [1.5 points]
- **Task**: Scale node radius based on degree
- **Requirements**:
  - Calculate node degrees manually (D3 v5 doesn't support d.weight)
  - Use linear or squared scale
  - Avoid extreme sizes (too small/large)

##### 3b. Color Gradients [1.5 points]
- **Task**: Color nodes based on degree
- **Requirements**:
  - At least 3 color gradations
  - Higher degree = darker/deeper colors
  - Lower degree = lighter colors
  - Use meaningful color scheme (Color Brewer)

#### 4. Node Pinning [6 points]
##### 4a. Pin on Drag [2 points]
- **Task**: Dragging fixes node position
- **Requirements**:
  - Pinned nodes not affected by layout algorithm
  - Pinned nodes can still be dragged
  - Other nodes move freely

##### 4b. Visual Distinction [1 point]
- **Task**: Mark pinned nodes visually
- **Requirements**:
  - Different color for pinned vs unpinned nodes

##### 4c. Unpin on Double-click [3 points]
- **Task**: Double-click unpins nodes
- **Requirements**:
  - Unpinned nodes move freely again
  - Remove visual marking

#### 5. GT Username [1 point]
- **Task**: Add GT username to top right corner
- **Requirements**:
  - Use `<text>` element with id="credit"
  - Display GT username (e.g., gburdell3)

### Technical Notes
- Use provided Q2.html as starting point
- Can split into Q2.html, Q2.css, Q2.js or keep as single file
- Relative paths for D3 libraries: `../lib/d3.v5.min.js`
- No absolute paths allowed

## Q3: Line Charts [15 points]

### Goal
Explore temporal patterns in BoardGameGeek data using line charts in D3 to compare rating growth and integrate board game rankings with different axis scales.

### Technology Requirements
- D3 Version 5 (provided in lib folder)
- Chrome v131.0.0 or higher
- Python HTTP server for local testing
- Dataset: boardgame_ratings.csv (provided)

### Implementation Plan

#### 1. Basic Line Chart [5 points]
- **Task**: Create line chart showing number of ratings from Nov 2016 to Aug 2020
- **Requirements**:
  - 8 board games: ['Catan', 'Dominion', 'Codenames', 'Terraforming Mars', 'Gloomhaven', 'Magic: The Gathering', 'Dixit', 'Monopoly']
  - Use d3.schemeCategory10() for colors
  - Add game names next to lines
  - X-axis: tick every 3 months, format as "Jan 17", "Apr 17", etc.
  - Chart title: "Number of Ratings 2016–2020"
  - X-axis label: "Month" (use D3.scaleTime())
  - Y-axis label: "Num of Ratings" (linear scale)
  - **CRITICAL**: Beware of silent date conversion in Excel

#### 2. Line Chart with Rankings [5 points]
- **Task**: Add ranking circle markers to line chart
- **Requirements**:
  - Same as part 1 but for games: ['Catan', 'Codenames', 'Terraforming Mars', 'Gloomhaven']
  - Circle markers every 3 months aligned with x-axis ticks
  - Show ranking text on circles
  - Add legend explaining circle markers
  - Chart title: "Number of Ratings 2016–2020 with Rankings"

#### 3. Different Axis Scales [5 points]
- **Task**: Create two additional charts with different y-axis scales
- **Requirements**:
  - **Chart 3a**: Square root scale for y-axis
    - Title: "Number of Ratings 2016–2020 (Square root Scale)"
    - Keep circle markers and legend from part 2
  - **Chart 3b**: Log scale for y-axis
    - Title: "Number of Ratings 2016–2020 (Log Scale)"
    - Set y-scale domain minimum to 1
    - Keep circle markers and legend from part 2
    - Add GT username at bottom right
  - All on single HTML page, one after another
  - Horizontal axes remain linear scale

### Technical Notes
- Use Margin Convention for chart dimensions
- Four charts total on single HTML page
- Follow specific DOM structure for autograder
- Handle 0s in data carefully for log scale
- No hardcoded scale domains

## Q4: Interactive Visualization [20 points]

### Goal
Create line charts in D3 with interactive elements displaying additional data, plus implement bar chart that appears on mouseover of line chart points.

### Technology Requirements
- D3 Version 5 (provided in lib folder)
- Chrome v131.0.0 or higher
- Python HTTP server for local testing
- Dataset: average-rating.csv (provided)

### Data Processing Requirements
- Round ratings down using Math.floor() (e.g., 7.71148 becomes 7)
- Aggregate count of board games by rating for each year
- Display lines for years 2015-2019 only
- Generate dummy values (0s) for missing datapoints
- All aggregation must be done in JavaScript (no CSV modification)

### Implementation Plan

#### 1. Basic Line Chart [3 points]
- **Task**: Create line chart summarizing game count by rating per year
- **Requirements**:
  - One line per year (2015-2019)
  - X-axis: ratings (linear scale, start at 0)
  - Y-axis: count of board games (linear scale, start at 0)
  - Auto-adjust upper limits based on data
  - Filled circles for each rating-count data point

#### 2. Styling and Legend [3 points]
- **Task**: Add styling, legend, title, and username
- **Requirements**:
  - Different color per line
  - Legend on right-hand side showing year-color mapping
  - Title: "Board games by Rating 2015–2019"
  - GT username beneath title

#### 3. Interactive Bar Chart [8 points]
- **Task**: Show horizontal bar chart on circle hover
- **Requirements**:
  - Display top 5 games with highest user ratings for hovered year/rating
  - Show below line chart
  - Bar length = number of users who rated the game
  - Auto-adjust axes based on data
  - Y-axis: game names (descending order by users_rated, first 10 chars only)
  - X-axis: number of users (linear scale)
  - X-axis label: "Number of users"
  - Y-axis label: "Games"
  - No bar chart when count = 0

#### 4. Bar Chart Styling [2 points]
- **Task**: Style bars and add grid lines
- **Requirements**:
  - Same color for all bars regardless of year/rating
  - Uniform bar thickness for specific year
  - Display grid lines
  - Title format: "Top 5 Most Rated Games of <Year> with Rating <Rating>"

#### 5. Mouseover Events [2 points]
- **Task**: Handle mouseover interactions
- **Requirements**:
  - Show bar chart and title only during mouseover
  - Enlarge hovered circle in line chart
  - No bar chart when count = 0, but still enlarge circle

#### 6. Mouseout Events [2 points]
- **Task**: Handle mouseout interactions
- **Requirements**:
  - Hide bar chart and title
  - Return circle to original size

### Technical Notes
- Follow specific DOM structure for autograder
- Use proper margin convention
- Single HTML page with both charts
- Handle edge cases (no data, fewer than 5 games)

## Q5: Choropleth Map of Wildlife Trafficking Incidents [25 points]

### Goal
Create a choropleth map in D3 to explore wildlife trafficking incidents per country by year.

### Technology Requirements
- D3 Version 5 (provided in lib folder)
- Chrome v131.0.0 or higher
- Python HTTP server for local testing
- Datasets: wildlife_trafficking.csv, world_countries.json

### Data Structure
- **wildlife_trafficking.csv**: Year, Country, Number of Incidents, Average Fine, Average Imprisonment
- **world_countries.json**: geoJSON with countries geometry collection

### Implementation Plan

#### 1. Choropleth Map Creation [20 points]

##### 1a. Dropdown Filter [5 points]
- **Task**: Create year selection dropdown
- **Requirements**:
  - Options from Year column in CSV
  - Sort in increasing order
  - Default to first option
  - Updates map and legend on selection

##### 1b. Map Visualization [10 points]
- **Task**: Create choropleth map with Natural Earth projection
- **Requirements**:
  - Color countries based on incident count for selected year
  - Countries with no data: gray color
  - Countries with data: quantile scale with 4 gradations
  - Darker colors = higher incident counts
  - Lighter colors = lower incident counts
  - Function name: `path` (for autograder)
  - Use Promise.all() to load both JSON and CSV

##### 1c. Legend [5 points]
- **Task**: Add vertical legend showing color-to-incident mapping
- **Requirements**:
  - Updates with quartiles of selected year
  - Values formatted to 2 decimal places
  - Exactly 4 color gradations
  - Rectangular legend bars
  - GT username beneath map
  - Recommended: use d3-legend.min.js

#### 2. Tooltip Implementation [5 points]
- **Task**: Add interactive tooltip using d3-tip.min library
- **Requirements**:
  - Show on hover: Country name, Year, Number of Incidents, Average Fine, Average Imprisonment
  - No data countries: display "N/A" for numeric values
  - Round Average Fine and Average Imprisonment to 2 decimals
  - Prevent flickering (position away from cursor or fixed position)
  - Single tooltip element (update content, don't create new)
  - Fully visible (not clipped at page edges)
  - Hide on mouseout

### DOM Structure Requirements

#### Q2 DOM Structure
```
(Standard D3 force-directed graph structure with proper IDs)
```

#### Q5 DOM Structure
```xml
<select id="yearDropdown">
  <option>year options</option>
</select>
<svg id="choropleth">
  <g id="countries">
    <path>country paths</path>
  </g>
  <g id="legend">legend elements</g>
</svg>
<div id="tooltip">tooltip content</div>
```

### Technical Implementation Notes

#### File Organization
- Setup local HTTP server in hw2-skeleton root folder
- Use relative paths for all D3 libraries: `../lib/filename`
- Use relative paths for datasets
- Can separate HTML, CSS, and JavaScript files

#### Key Technical Requirements
- Use D3 Version 5 only (provided libraries)
- Test in Chrome v131+
- Follow margin convention for charts
- Auto-grade friendly DOM structure
- No hardcoded values for scales/axes

#### Color Schemes
- Use Color Brewer for meaningful gradients
- Q2: At least 3 gradations for node degrees
- Q5: Exactly 4 gradations for quartiles

#### Interactivity
- Q2: Drag to pin, double-click to unpin, visual feedback
- Q5: Hover tooltips, dropdown filtering, legend updates

### Testing Strategy
1. Setup local HTTP server: `python -m http.server`
2. Test in Chrome v131+
3. Verify all interactive features work
4. Check DOM structure matches requirements
5. Test edge cases (no data, extreme values)
6. Validate relative paths work
7. Ensure autograder compatibility

### Submission Requirements
- Q2: Submit HTML/JS/CSS files (no libraries or CSV)
- Q5: Submit HTML/JS/CSS files (no libraries or CSV/JSON)
- Use Gradescope for submission
- Auto-graded upon submission

### Agent Assignment Plan
1. **Q2 Implementation**: Assign to `javascript-pro` agent for D3 force-directed graph
2. **Q3 Implementation**: Assign to `javascript-pro` agent for D3 line charts with multiple scales
3. **Q4 Implementation**: Assign to `javascript-pro` agent for D3 interactive visualization
4. **Q5 Implementation**: Assign to `javascript-pro` agent for D3 choropleth map
5. **Testing & Validation**: Assign to `debugger` agent for cross-browser testing
6. **Code Review**: Assign to `code-reviewer` agent for final review

This plan ensures systematic implementation of all four questions (Q2-Q5) with proper attention to technical requirements, DOM structure, and interactive features.

### DOM Structure Requirements

#### Q3 DOM Structure
```xml
<svg id="svg-a"> <!-- Q3.1 -->
  <text id="title-a">chart title</text>
  <g id="plot-a">
    <g id="lines-a">plot lines, line labels</g>
    <g id="x-axis-a">x-axis elements</g>
    <g id="y-axis-a">y-axis elements</g>
  </g>
</svg>
<svg id="svg-b"> <!-- Q3.2 -->
  <text id="title-b">chart title</text>
  <g id="plot-b">
    <g id="lines-b">plot lines, line labels</g>
    <g id="x-axis-b">x-axis elements</g>
    <g id="y-axis-b">y-axis elements</g>
    <g id="symbols-b">circle markers</g>
  </g>
  <g id="legend-b">legend elements</g>
</svg>
<svg id="svg-c-1"> <!-- Q3.3-1 (square root) -->
<svg id="svg-c-2"> <!-- Q3.3-2 (log scale) -->
<div id="signature">GT username</div>
```

#### Q4 DOM Structure
```xml
<svg id="line_chart">
  <g id="container">
    <g id="lines">line elements</g>
    <g id="x-axis-lines">x-axis</g>
    <g id="y-axis-lines">y-axis</g>
    <g id="circles">circle elements</g>
    <text id="line_chart_title">title</text>
    <text id="credit">GT username</text>
    <g id="legend">legend elements</g>
    <text>axis labels</text>
  </g>
</svg>
<div id="bar_chart_title">bar chart title</div>
<svg id="bar_chart">
  <g id="container_2">
    <g id="bars">bar elements</g>
    <g id="x-axis-bars">x-axis</g>
    <g id="y-axis-bars">y-axis</g>
    <text id="bar_x_axis_label">x label</text>
    <text id="bar_y_axis_label">y label</text>
  </g>
</svg>
```