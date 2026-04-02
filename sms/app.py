import streamlit as st
import re
import pymysql
import pandas as pd


def dbConnection():
    try:
        con = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="std_manag_sys"
        )
        print("Database Connected Successfully")
        return con
    except Exception as e:
        print("Connection Error:", e)


def create_table():
    con = dbConnection()
    curObj = con.cursor()

    curObj.execute(
        """create table if not exists student(
        id int primary key auto_increment,
        name varchar(20) not null,
        age int not null,
        email varchar(50) unique not Null,
        course varchar(50)
    )
    """
    )

    con.commit()
    curObj.close()
    con.close()


create_table()


st.set_page_config(page_title="Student Management System", layout="centered")
st.title("Student Management System")
st.write("Manage Student records easily with a simple and interactive interface")

# Sidebar
menu = st.sidebar.selectbox(
    "Meu",
    ["Home", "Add Student", "View Students", "Update Student", "Delete Student"]
)

st.write(f"You selected: {menu}")


def home():
    st.header("Welcome to the Student Management System.")
    # st.write("This application helps you manage student records efficiently.")

    st.subheader("Features")
    st.write("Add new student")
    st.write("View Student details")
    st.write("Update student information")
    st.write("Delete student records")

    st.subheader("Instructions")
    st.write("Use the sidebar to navigate between different options.")


def add_students():
    st.header("Add Student")

    id = st.number_input("Enter Id")
    name = st.text_input("Enter Name")
    age = st.number_input("Enter age")
    email = st.text_input("Enter Email")

    # Email Validation
    if email:
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.success("Valid Email")
        else:
            st.error("Invalid Email")

    course = st.text_input("Enter Course")

    if st.button("Add Student"):
        if name and email and course:
            con = dbConnection()
            curObj = con.cursor()

            query = "insert into student (id, name, age, email, course)values(%s, %s, %s, %s, %s)"
            values = (id, name, age, email, course)
            curObj.execute(query, values)
            con.commit()

            st.success(f"Student {name} added successfully!")

            curObj.close()
            con.close()
        else:
            st.error("Please Fill all required fields")


def view_students():
    st.header("Student List")

    con = dbConnection()
    curObj = con.cursor()

    query = "select * from student"
    # curObj.execute(query)
    df = pd.read_sql(query, con)

    # data = curObj.fetchall()
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("No student records found")

    # if data:
    #     st. table(data)
    # else:
    #     st.warning("No student records found")
    # curObj.close()
    con.close()
    
def update_student():
    st.header("Update Student")
    
    id = st.number_input("Enter Student id to Update")
    
    if st.button("Fetch Student"):
        con = dbConnection()
        curObj = con.cursor()
        
        query = "select * from student where id=%s"
        curObj.execute(query, (id,))
        data = curObj.fetchone()
        
        if data:
            # pass
            st.session_state["update_data"] = data
        else:
            st.error("Student not found")
        curObj.close()
        con.close()
        
    # st.write("Session State:", st.session_state)
        
    if "update_data" in st.session_state:
        data = st.session_state["update_data"]
        
        name = st.text_input("Enter Name", value=data[1])
        age = st.number_input("Enter Age", value=data[2])
        email = st.text_input("Enter Email", value=data[3])
        course = st.text_input("Enter Course", value=data[4])
        
        if st.button("Update Student"):
            con = dbConnection()
            curObj = con.cursor()
            
            query = """
            update student
            set name=%s, age=%s, email=%s, course=%s
            where id=%s
            """
            
            values = (name, age, email, course, id)
            
            curObj.execute(query, values)
            con.commit() 
                
            st.success("Studdent updated successfully!")
            
            curObj.close()
            con.close()
        
        # del st.session_state["update_data"]
        # st.rerun()
        
        # if "update_data" in st.session_state:
        #     if st.button("Back"):
        #         del st.session_state["update_data"]
        #         st.rerun() 


if menu == "Home":
    home()

elif menu == "Add Student":
    add_students()
    
elif menu == "View Students":
    view_students()
    
elif menu == "Update Student":
    update_student()
    
elif menu == "Delete Student":
    st.info("Delete feature coming soon")