import streamlit as st
from io import StringIO

from settings import *
from world import World
from character import Character
from state_management import load_from_json, create_json_data
from items import ITEMS_DATABASE

# Initial page config

st.set_page_config(
    page_title=GAME_TITLE,
    layout="wide",
    initial_sidebar_state="expanded",
)

if 'player_character' not in st.session_state:
    st.session_state['player_character'] = Character()

if 'world' not in st.session_state:
    st.session_state['world'] = World()


@st.cache_data
def load_save(uploaded_file):
    json_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
    st.session_state['player_character'], st.session_state['world'] = load_from_json(json_data)


def main():
    cs_sidebar()

    cs_body()
    return None


def cs_sidebar():
    st.sidebar.header(GAME_TITLE)
    st.sidebar.markdown(GAME_SUBTITLE)
    if st.sidebar.button("Reset game"):
        st.session_state['player_character'] = Character()
        st.session_state['world'] = World()
        st.rerun()
    json_data = create_json_data(st.session_state['player_character'], st.session_state['world'])
    st.sidebar.download_button(
        label="Download save as JSON",
        data=json_data,
        file_name="character_world.json",
        mime="application/json"
    )
    uploaded_file = st.sidebar.file_uploader("Upload a JSON file", type="json")

    if uploaded_file is not None:
        load_save(uploaded_file)
        st.write("Save loaded.")

    st.sidebar.write("Dev only:")
    if st.sidebar.button("God mode"):
        st.session_state['player_character'].money = 5000
        st.session_state['player_character'].abilities["Strength"] = 100
        st.session_state['player_character'].abilities["Wisdom"] = 100
        st.session_state['player_character'].abilities["Charisma"] = 100


def cs_body():
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.container(border=True):
            col11, col12, col13 = st.columns([4, 2, 3])
            with col11:
                st.markdown(st.session_state['player_character'].display())
                st.markdown(f"  \r :moneybag: Coins: {st.session_state['player_character'].money}")
                with st.popover(label="Inventory"):
                    if len(st.session_state['player_character'].inventory) == 0:
                        st.markdown("Your inventory is empty.")
                    else:
                        item_types_displayed = []
                        for i, item in enumerate(st.session_state['player_character'].inventory):
                            if item not in item_types_displayed:
                                item_types_displayed.append(item)
                                with st.container(border=True):
                                    item_object = ITEMS_DATABASE[item]()
                                    no = st.session_state['player_character'].inventory.count(item)
                                    if no > 1:
                                        item_str = f"**({no}x) {item_object.name}**"
                                    else:
                                        item_str = f"**{item_object.name}**"
                                    if item_object.description != "":
                                        item_str += f": {item_object.description}"
                                    st.markdown(item_str)
                                    if item_object.type == "potion":
                                        if st.button("Drink.", key=f"inv_item{i}"):
                                            item_object.use(st.session_state['player_character'], st.session_state['world'])
                                            st.session_state['player_character'].inventory.remove(item)
                                            st.rerun()
                                    if no > 1:
                                        delete_button = "Throw away one."
                                    else:
                                        delete_button = "Throw away."
                                    if st.button(delete_button, key=f"inv_item_delete_{i}"):
                                        st.session_state['player_character'].inventory.remove(item)
                                        st.rerun()
            with col12:
                st.markdown(st.session_state['player_character'].display2())
            with col13:
                st.markdown(st.session_state['player_character'].display3())

    with col2:
        # Notes section
        with st.container(border=True):
            st.markdown("**Traits**:  \r  \r")
            traitslist = ""
            for trait in st.session_state['player_character'].traits:
                traitslist += trait + "; "
            st.markdown(traitslist)

    # Main section with multiple containers
    with st.container():
        with st.container(border=True):
            colm1, colm2 = st.columns([3, 2])
            with colm1:
                st.markdown(st.session_state['world'].display())
                st.markdown(st.session_state['world'].message)
            with colm2:
                if st.session_state['world'].image is not None:
                    st.image(st.session_state['world'].image)
            st.markdown(st.session_state['player_character'].display_notes())
        quests = []
        quests += st.session_state['player_character'].generate_quests(st.session_state['world'])
        quests += st.session_state['world'].generate_quests(st.session_state['player_character'])
        for quest in quests:
            with st.container(border=True):
                if quest.title != "":
                    st.subheader(quest.title)
                if quest.title in ["Job board.", "Playfair Square."]:
                    with st.expander(f"Show: {quest.title}", expanded=False):
                        display_quest(quest)
                else:
                    display_quest(quest)


def display_quest(quest):

    st.write(quest.content)
    for action_key in quest.actions:
        action = quest.actions[action_key]
        with st.container(border=True):
            if action.image is None:
                col12, col13 = st.columns([4, 1])
            else:
                if action.image_size is not None:
                    col11, col12, col13 = st.columns([2*action.image_size, 2*(1-action.image_size), 1.0])
                else:
                    col11, col12, col13 = st.columns([2, 2, 1])
                with col11:
                    st.image(action.image)
            with col12:
                st.write(action.content)
            with col13:
                if st.button(action.button, key=action_key):
                    quest.actions[action_key].execute(st.session_state['player_character'],
                                                      st.session_state['world'])
                    st.rerun()


if __name__ == "__main__":
    main()
