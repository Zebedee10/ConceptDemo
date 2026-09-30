import re

import plotly.graph_objects as go

import streamlit as st



from streamlit_plotly_events2 import (

    plotly_events,

)



from components.ui import render_html



from services.taxonomy_service import (

    TaxonomyService,

)





# ============================================================

# LEVEL 1 COLOURS

# ============================================================



LEVEL_1_COLOURS = [

    "#356CC9",

    "#7DB3E8",

    "#EA4335",

    "#ECA1A1",

    "#5CA89D",

    "#86D993",

    "#F28E2B",

    "#F2CC70",

    "#6747C2",

    "#D4D9E3",

]



DEFINING_COLOUR = "#D9DEE7"





# ============================================================

# LEVEL 1 GOVERNANCE STATUS

# ============================================================



LEVEL_1_STATUS = {

    "Tax_L1": "approved",

    "Tax_L2": "approved",

    "Tax_L3": "approved",

    "Tax_L4": "approved",

    "Tax_L5": "approved",

    "Tax_L6": "approved",

    "Tax_L7": "defining",

    "Tax_L8": "defining",

    "Tax_L9": "defining",

    "Tax_L10": "defining",

}





def get_domain_status(

    category_id: str,

) -> str:



    return LEVEL_1_STATUS.get(

        category_id,

        "defining",

    )





def get_domain_colour(

    category_id: str,

    index: int,

) -> str:



    status = get_domain_status(

        category_id

    )



    if status == "approved":



        return LEVEL_1_COLOURS[

            index

            % len(LEVEL_1_COLOURS)

        ]



    return DEFINING_COLOUR





# ============================================================

# STATE MANAGEMENT

# ============================================================



def initialise_taxonomy_state(

    service: TaxonomyService,

):



    (

        default_l1,

        default_l2,

        default_l3,

    ) = service.get_initial_path()



    if (

        "taxonomy_selected_l1"

        not in st.session_state

    ):

        st.session_state.taxonomy_selected_l1 = (

            default_l1

        )



    if (

        "taxonomy_selected_l2"

        not in st.session_state

    ):

        st.session_state.taxonomy_selected_l2 = (

            default_l2

        )



    if (

        "taxonomy_selected_l3"

        not in st.session_state

    ):

        st.session_state.taxonomy_selected_l3 = (

            default_l3

        )





def select_level_1(

    service: TaxonomyService,

    value: str,

):



    (

        level_1,

        level_2,

        level_3,

    ) = service.get_path_for_level_1(

        value

    )



    st.session_state.taxonomy_selected_l1 = (

        level_1

    )



    st.session_state.taxonomy_selected_l2 = (

        level_2

    )



    st.session_state.taxonomy_selected_l3 = (

        level_3

    )





def select_level_2(

    service: TaxonomyService,

    value: str,

):



    (

        level_1,

        level_2,

        level_3,

    ) = service.get_path_for_level_2(

        st.session_state.taxonomy_selected_l1,

        value,

    )



    st.session_state.taxonomy_selected_l1 = (

        level_1

    )



    st.session_state.taxonomy_selected_l2 = (

        level_2

    )



    st.session_state.taxonomy_selected_l3 = (

        level_3

    )





def select_level_3(

    value: str,

):



    st.session_state.taxonomy_selected_l3 = (

        value

    )






# ============================================================
# SEARCH
# ============================================================


def build_search_index(
    service: TaxonomyService,
) -> tuple[list[dict], dict[str, list[dict]]]:

    """
    Build search choices for categories and technologies.

    Categories are represented by their taxonomy path.
    Technologies are represented once by name, with their category
    occurrences retained separately so duplicate placements can be
    resolved after the technology is selected.
    """

    category_results = []
    technology_paths: dict[str, list[dict]] = {}
    technology_display_names: dict[str, str] = {}

    for level_1 in service.get_level_1_categories():

        category_results.append(
            {
                "result_type": "Category",
                "label": f"Cat: {level_1.name}",
                "level_1_id": level_1.id,
                "level_2_id": None,
                "level_3_id": None,
            }
        )

        for level_2 in service.get_level_2_categories(
            level_1.id
        ):

            level_2_path = (
                f"{level_1.name} → {level_2.name}"
            )

            category_results.append(
                {
                    "result_type": "Category",
                    "label": f"Cat: {level_2_path}",
                    "level_1_id": level_1.id,
                    "level_2_id": level_2.id,
                    "level_3_id": None,
                }
            )

            for level_3 in service.get_level_3_categories(
                level_1.id,
                level_2.id,
            ):

                path = (
                    f"{level_1.name} → "
                    f"{level_2.name} → "
                    f"{level_3.name}"
                )

                category_results.append(
                    {
                        "result_type": "Category",
                        "label": f"Cat: {path}",
                        "level_1_id": level_1.id,
                        "level_2_id": level_2.id,
                        "level_3_id": level_3.id,
                    }
                )

                detail = service.get_level_3_detail(
                    level_1.id,
                    level_2.id,
                    level_3.id,
                )

                if detail is None:
                    continue

                for technology in detail.technologies:

                    technology_key = (
                        technology.name.casefold()
                    )

                    technology_display_names.setdefault(
                        technology_key,
                        technology.name,
                    )

                    technology_paths.setdefault(
                        technology_key,
                        [],
                    ).append(
                        {
                            "path": path,
                            "level_1_id": level_1.id,
                            "level_2_id": level_2.id,
                            "level_3_id": level_3.id,
                        }
                    )

    search_results = category_results.copy()

    for technology_key, technology_name in sorted(
        technology_display_names.items(),
        key=lambda item: item[1].casefold(),
    ):
        search_results.append(
            {
                "result_type": "Technology",
                "label": f"Tech: {technology_name}",
                "technology_key": technology_key,
            }
        )

    search_results.sort(
        key=lambda item: item["label"].casefold()
    )

    return search_results, technology_paths


def apply_search_result(
    service: TaxonomyService,
    result: dict,
):

    """Open the Navigator at the path represented by a result."""

    level_1_id = result["level_1_id"]
    level_2_id = result["level_2_id"]
    level_3_id = result["level_3_id"]

    if level_3_id:
        st.session_state.taxonomy_selected_l1 = level_1_id
        st.session_state.taxonomy_selected_l2 = level_2_id
        st.session_state.taxonomy_selected_l3 = level_3_id

    elif level_2_id:
        st.session_state.taxonomy_selected_l1 = level_1_id
        select_level_2(
            service,
            level_2_id,
        )

    else:
        select_level_1(
            service,
            level_1_id,
        )

    st.session_state.pop(
        "taxonomy_pending_technology",
        None,
    )


def handle_search_selection(
    service: TaxonomyService,
    result_by_label: dict[str, dict],
    technology_paths: dict[str, list[dict]],
):

    """Apply a search choice as soon as the selectbox changes."""

    selected_label = st.session_state.get(
        "taxonomy_search_selection"
    )

    if not selected_label:
        return

    selected_result = result_by_label.get(
        selected_label
    )

    if selected_result is None:
        return

    if (
        selected_result["result_type"]
        == "Category"
    ):
        apply_search_result(
            service,
            selected_result,
        )

        # Clear the completed search on the next run.  This is
        # done before the widget is rebuilt so Streamlit does not
        # repeatedly process the same category selection.
        st.session_state.taxonomy_clear_search = True
        return

    technology_key = selected_result[
        "technology_key"
    ]

    occurrences = technology_paths.get(
        technology_key,
        [],
    )

    if len(occurrences) == 1:
        apply_search_result(
            service,
            occurrences[0],
        )
        st.session_state.taxonomy_clear_search = True
        return

    st.session_state.taxonomy_pending_technology = (
        technology_key
    )


def render_search(
    service: TaxonomyService,
):

    """
    Render a native searchable selector.

    Streamlit filters the options interactively as the user types.
    Category choices contain only taxonomy paths and technology
    choices contain only technology names.
    """

    search_results, technology_paths = (
        build_search_index(service)
    )

    result_by_label = {
        result["label"]: result
        for result in search_results
    }

    # A completed result is cleared before the widget is created.
    # This prevents a previously selected category from being
    # re-processed on every Streamlit rerun.
    if st.session_state.pop(
        "taxonomy_clear_search",
        False,
    ):
        st.session_state.taxonomy_search_selection = None

    st.selectbox(
        "Search the STL",
        options=list(result_by_label.keys()),
        index=None,
        placeholder="Search categories or technologies...",
        key="taxonomy_search_selection",
        label_visibility="collapsed",
        on_change=handle_search_selection,
        args=(
            service,
            result_by_label,
            technology_paths,
        ),
    )

    pending_technology = st.session_state.get(
        "taxonomy_pending_technology"
    )

    if not pending_technology:
        return

    occurrences = technology_paths.get(
        pending_technology,
        [],
    )

    if len(occurrences) <= 1:
        return

    st.caption(
        "This technology appears in more than one category. "
        "Select the category you want to open."
    )

    for index, occurrence in enumerate(occurrences):

        if st.button(
            f"Cat: {occurrence['path']}",
            key=(
                "taxonomy_search_technology_path_"
                f"{pending_technology}_{index}"
            ),
            use_container_width=True,
        ):
            apply_search_result(
                service,
                occurrence,
            )
            st.session_state.taxonomy_clear_search = True
            st.rerun()


# ============================================================

# LEVEL 1 LABEL FORMATTING

# ============================================================


def wrap_wheel_label(
    label: str,
    max_chars_per_line: int = 14,
) -> str:

    """
    Wrap longer wheel labels over multiple horizontal lines.

    Breaks are made at common separators where possible so the
    displayed wording remains readable without changing the
    underlying category value used for selection.
    """

    if len(label) <= max_chars_per_line:
        return label

    chunks = re.findall(
        r"[^ _/-]+[ _/-]*",
        label,
    )

    if not chunks:
        return label

    lines = []
    current_line = ""

    for chunk in chunks:

        candidate = (
            current_line + chunk
        )

        if (
            current_line
            and len(candidate)
            > max_chars_per_line
        ):
            lines.append(
                current_line.rstrip()
            )
            current_line = chunk.lstrip()
        else:
            current_line = candidate

    if current_line:
        lines.append(
            current_line.rstrip()
        )

    return "<br>".join(lines)


# ============================================================

# LEVEL 1 WHEEL

# ============================================================



def render_level_1(

    service: TaxonomyService,

):



    render_html(

        """

        <div class="panel-subheading"

             style="

                margin-bottom:8px;

                font-size:13px;

             ">

            Select a technology domain

        </div>

        """

    )



    categories = (

        service.get_level_1_categories()

    )



    category_ids = [

        category.id

        for category in categories

    ]



    display_category_names = [

        wrap_wheel_label(
            category.name
        )

        for category in categories

    ]



    selected = (

        st.session_state.taxonomy_selected_l1

    )



    pull = [

        0.07

        if category.id == selected

        else 0

        for category in categories

    ]



    colours = [

        get_domain_colour(

            category.id,

            index,

        )

        for index, category

        in enumerate(categories)

    ]



    wheel = go.Figure(

        go.Pie(

            labels=display_category_names,



            values=[

                1

                for _ in categories

            ],



            hole=0.45,



            sort=False,



            direction="clockwise",



            pull=pull,



            textinfo="label",



            textposition="inside",


            insidetextorientation="horizontal",



            hoverinfo="none",



            marker=dict(

                colors=colours,



                line=dict(

                    color="#FFFFFF",

                    width=2,

                ),

            ),



            insidetextfont=dict(

                size=12,

                color="#0B1F3A",

            ),

        )

    )



    wheel.update_layout(



        height=380,



        margin=dict(

            l=0,

            r=0,

            t=0,

            b=0,

        ),



        paper_bgcolor="rgba(0,0,0,0)",



        plot_bgcolor="rgba(0,0,0,0)",



        showlegend=False,



        template="none",



        font=dict(

            size=12,

            color="#183153",

        ),


        uniformtext=dict(
            minsize=11,
            mode="show",
        ),



        annotations=[

            dict(

                x=0.5,

                y=0.5,



                text=(

                    "<b>"

                    "Technology"

                    "<br>"

                    "Taxonomy"

                    "</b>"

                ),



                showarrow=False,



                align="center",



                font=dict(

                    size=17,

                    color="#183153",

                ),

            )

        ],

    )



    clicked_points = plotly_events(



        wheel,



        click_event=True,



        select_event=False,



        hover_event=False,



        override_height=380,



        config={

            "displayModeBar": False,

            "displaylogo": False,

            "scrollZoom": False,

            "responsive": True,

        },



        key="taxonomy_level_1_wheel",

    )



    if clicked_points:



        clicked_point = (

            clicked_points[0]

        )



        point_number = (

            clicked_point.get(

                "pointNumber"

            )

        )



        if point_number is None:



            point_number = (

                clicked_point.get(

                    "pointIndex"

                )

            )



        if (

            point_number is not None

            and 0 <= point_number

            < len(category_ids)

        ):



            clicked_id = (

                category_ids[

                    point_number

                ]

            )



            if clicked_id != selected:



                select_level_1(

                    service,

                    clicked_id,

                )



                st.rerun()



    render_html(

        """

        <div style="

            display:flex;

            align-items:center;

            justify-content:center;

            gap:18px;

            margin-top:3px;

            font-size:12px;

            color:#66758A;

        ">



            <div style="

                display:flex;

                align-items:center;

                gap:6px;

            ">

                <span style="

                    width:10px;

                    height:10px;

                    border-radius:50%;

                    background:#356CC9;

                    display:inline-block;

                "></span>

                Approved

            </div>



            <div style="

                display:flex;

                align-items:center;

                gap:6px;

            ">

                <span style="

                    width:10px;

                    height:10px;

                    border-radius:50%;

                    background:#D9DEE7;

                    display:inline-block;

                    border:1px solid #C8CFD9;

                "></span>

                Still to be defined

            </div>



        </div>

        """

    )





# ============================================================

# LEVEL 2

# ============================================================



def render_level_2(

    service: TaxonomyService,

):



    selected_l1 = (

        st.session_state.taxonomy_selected_l1

    )



    categories = (

        service.get_level_2_categories(

            selected_l1

        )

    )



    render_html(

        f"""

        <div style="

            display:flex;

            justify-content:space-between;

            align-items:center;

            gap:12px;

            margin-bottom:8px;

        ">



            <div class="panel-subheading"

                 style="margin-bottom:0;">

                Categories in {selected_l1}

            </div>



            <div class="category-badge">

                {len(categories)} categories

            </div>



        </div>

        """

    )



    if not categories:



        st.info(

            "No Level 2 categories found."

        )



        return



    for category in categories:



        selected = (

            category.id

            == st.session_state.taxonomy_selected_l2

        )



        label = (

            f"✓  {category.name}"

            if selected

            else f"›  {category.name}"

        )



        if st.button(

            label,



            key=(

                f"taxonomy_level2_"

                f"{category.id}"

            ),



            type=(

                "primary"

                if selected

                else "secondary"

            ),

        ):



            select_level_2(

                service,

                category.id,

            )



            st.rerun()





# ============================================================

# LEVEL 3

# ============================================================



def render_level_3(

    service: TaxonomyService,

):



    selected_l1 = (

        st.session_state.taxonomy_selected_l1

    )



    selected_l2 = (

        st.session_state.taxonomy_selected_l2

    )



    if selected_l2:



        categories = (

            service.get_level_3_categories(

                selected_l1,

                selected_l2,

            )

        )



    else:



        categories = []



    render_html(

        f"""

        <div style="

            display:flex;

            justify-content:space-between;

            align-items:center;

            gap:12px;

            margin-bottom:8px;

        ">



            <div class="panel-subheading"

                 style="margin-bottom:0;">

                Categories in {selected_l2 or ""}

            </div>



            <div class="category-badge">

                {len(categories)} categories

            </div>



        </div>

        """

    )



    if not categories:



        st.info(

            "No Level 3 categories found."

        )



        return



    for category in categories:



        selected = (

            category.id

            == st.session_state.taxonomy_selected_l3

        )



        label = (

            f"✓  {category.name}"

            if selected

            else f"›  {category.name}"

        )



        if st.button(

            label,



            key=(

                f"taxonomy_level3_"

                f"{category.id}"

            ),



            type=(

                "primary"

                if selected

                else "secondary"

            ),

        ):



            select_level_3(

                category.id

            )



            st.rerun()





# ============================================================

# DETAIL

# ============================================================



def render_detail(

    service: TaxonomyService,

):



    selected_l1 = (

        st.session_state.taxonomy_selected_l1

    )



    selected_l2 = (

        st.session_state.taxonomy_selected_l2

    )



    selected_l3 = (

        st.session_state.taxonomy_selected_l3

    )



    st.divider()



    domain_status = get_domain_status(

        selected_l1

    )



    if domain_status == "defining":



        render_html(

            """

            <div class="detail-panel">



                <div class="detail-title">

                    Strategic technologies still to be defined

                </div>



                <div class="detail-description">

                    Strategic technologies for this domain

                    are still being defined.

                </div>



            </div>

            """

        )



        return



    if not selected_l3:



        st.info(

            "Select a category to see its details."

        )



        return



    detail = (

        service.get_level_3_detail(

            selected_l1,

            selected_l2,

            selected_l3,

        )

    )



    if detail is None:



        st.warning(

            "No information is available "

            "for this category."

        )



        return



    render_html(

        f"""

        <div class="detail-panel">



            <div class="detail-title">

                {detail.level_3.name}

            </div>



            <div class="detail-description">

                {

                    detail.level_3.description

                    or

                    "No description has been provided."

                }

            </div>



        </div>

        """

    )



    render_html(

        f"""

        <div style="

            margin-top:15px;

            margin-bottom:7px;

            font-size:17px;

            font-weight:700;

            color:#0B1F3A;

        ">

            Strategic Technologies



            <span style="

                color:#7D8998;

                font-size:12px;

                font-weight:500;

                margin-left:6px;

            ">

                {len(detail.technologies)} technologies

            </span>

        </div>

        """

    )



    if not detail.technologies:



        st.info(

            "No strategic technologies are recorded."

        )



        return



    cards_per_row = 4



    for row_start in range(

        0,

        len(detail.technologies),

        cards_per_row,

    ):



        current_row = (

            detail.technologies[

                row_start:

                row_start + cards_per_row

            ]

        )



        columns = st.columns(

            cards_per_row,

            gap="small",

        )



        for (

            column,

            technology,

        ) in zip(

            columns,

            current_row,

        ):



            with column:



                render_html(

                    f"""

                    <div class="tech-card">



                        <div class="tech-name">

                            {technology.name}

                        </div>



                        <div class="tech-description">

                            {technology.description}

                        </div>



                    </div>

                    """

                )





# ============================================================

# PAGE ENTRY POINT

# ============================================================



def render_page(

    service: TaxonomyService,

):



    initialise_taxonomy_state(

        service

    )



    st.title(

        "STL Navigator"

    )



    search_left, search_right = st.columns(

        [1.35, 2],

        gap="medium",

    )



    with search_right:

        render_search(

            service

        )



    (

        column_l1,

        column_l2,

        column_l3,

    ) = st.columns(

        [1.35, 1, 1],

        gap="medium",

    )



    with column_l1:



        render_level_1(

            service

        )



    with column_l2:



        render_level_2(

            service

        )



    with column_l3:



        render_level_3(

            service

        )



    render_detail(

        service

    )