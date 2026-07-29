d = {
     "message": "success",
     "payload":{"attendance": 5}
}

# print(d.values())
# print(d.keys())

inner_dict = d.get("payload") # {"attendance": 5}
print(inner_dict)
print(type(inner_dict))
print(inner_dict.get("attendance"))
print(d.get("payload").get("attendance"))
d2 = {
     "message": "success",
     "payload": ""
}

if type(d2.get("payload")) == dict:
    print(d2.get("payload").get("attendance"))

d3 = {
     "message": "success"
    }

print(d3.get("payload", {}).get("attendance", "no attendance"))
# print(d3["payload"]["attendance"])

students_info = {
    "code": 200,
    "message": "Success", # Success or Failed
    "payload": {
        "attendance": {
            "id": 11701213,
            "taken_by": 93018912,
            "taken_by_name": "Kasi Yedumati", #lecturer
            "class_date": 1784658600,
            "start_time": 570,
            "end_time": 660,
            "status": 1,
            "taken_at": 1784692925,
            "signin_by": 93018912,
            "signin_by_name": "Kasi Yedumati",
            "class_name": "Python",
            "class_id": 555840,
            "total_students": 10,
            "present": 6,
            "admin_data": {
                "canChangeTime": None,
                "canChangeDate": None,
                "pay": 0
            },
            "student_data": [
                {
                    "studentId": 93161455,
                    "name": "C SAI SREYAS",
                    "status": 1,
                    "remarks": "",
                    "user_status": 1,
                    "user_status_time": 1784694072,
                    "user_rating": 0,
                    "user_comments": "",
                    "parent_id": 0,
                    "parent_name": "",
                    "parent_status": 0,
                    "parent_status_time": 0,
                    "parent_rating": 0,
                    "parent_comments": "",
                    "img_url": "",
                    "user_state": 1,
                    "contact_number": "9494387779",
                    "reg_id": "25966",
                    "p_img_url": "",
                    "org_status": 2,
                    "email": "saisreyasc@gmail.com",
                    "learner_status": 1,
                    "is_nonmandatory_session": 0
                },
                {
                    "studentId": 93168101,
                    "name": "Divya",
                    "status": -1,
                    "remarks": "",
                    "user_status": 0,
                    "user_status_time": -1,
                    "user_rating": 0,
                    "user_comments": "",
                    "parent_id": 0,
                    "parent_name": "",
                    "parent_status": 0,
                    "parent_status_time": -1,
                    "parent_rating": 0,
                    "parent_comments": "",
                    "img_url": "",
                    "user_state": 1,
                    "contact_number": "9493801015",
                    "reg_id": "25992",
                    "p_img_url": "",
                    "org_status": 2,
                    "email": "divyanagireddygari0114@gmail.com",
                    "learner_status": 1,
                    "is_nonmandatory_session": 0
                },
                {
                    "studentId": 93086350,
                    "name": "Gelli.Dharani Chandra Sekhar Reddy",
                    "status": 1,
                    "remarks": "",
                    "user_status": 1,
                    "user_status_time": 1784693223,
                    "user_rating": 0,
                    "user_comments": "",
                    "parent_id": 0,
                    "parent_name": "",
                    "parent_status": 0,
                    "parent_status_time": 0,
                    "parent_rating": 0,
                    "parent_comments": "",
                    "img_url": "",
                    "user_state": 1,
                    "contact_number": "8121702104",
                    "reg_id": "25793",
                    "p_img_url": "",
                    "org_status": 2,
                    "email": "gellichandrasekharreddy321@gmail.com",
                    "learner_status": 1,
                    "is_nonmandatory_session": 0
                },
                {
                    "studentId": 93151962,
                    "name": "Lehyamjali Pujala",
                    "status": 1,
                    "remarks": "",
                    "user_status": 1,
                    "user_status_time": 1784692955,
                    "user_rating": 0,
                    "user_comments": "",
                    "parent_id": 0,
                    "parent_name": "",
                    "parent_status": 0,
                    "parent_status_time": 0,
                    "parent_rating": 0,
                    "parent_comments": "",
                    "img_url": "",
                    "user_state": 1,
                    "contact_number": "9490666276",
                    "reg_id": "25959",
                    "p_img_url": "",
                    "org_status": 2,
                    "email": "anjalipujala057@gmail.com",
                    "learner_status": 1,
                    "is_nonmandatory_session": 0
                },
                {
                    "studentId": 93089281,
                    "name": "Maram Bhuvanesh",
                    "status": 1,
                    "remarks": "",
                    "user_status": 1,
                    "user_status_time": 1784693115,
                    "user_rating": 0,
                    "user_comments": "",
                    "parent_id": 0,
                    "parent_name": "",
                    "parent_status": 0,
                    "parent_status_time": 0,
                    "parent_rating": 0,
                    "parent_comments": "",
                    "img_url": "",
                    "user_state": 1,
                    "contact_number": "8688734386",
                    "reg_id": "25801",
                    "p_img_url": "",
                    "org_status": 2,
                    "email": "marambhuvanesh@gmail.com",
                    "learner_status": 1,
                    "is_nonmandatory_session": 0
                },
                {
                    "studentId": 93150522,
                    "name": "Mula Harika",
                    "status": -1,
                    "remarks": "",
                    "user_status": 0,
                    "user_status_time": -1,
                    "user_rating": 0,
                    "user_comments": "",
                    "parent_id": 0,
                    "parent_name": "",
                    "parent_status": 0,
                    "parent_status_time": -1,
                    "parent_rating": 0,
                    "parent_comments": "",
                    "img_url": "",
                    "user_state": 1,
                    "contact_number": "7815983095",
                    "reg_id": "25957",
                    "p_img_url": "",
                    "org_status": 2,
                    "email": "mulaharikareddy@gmail.com",
                    "learner_status": 1,
                    "is_nonmandatory_session": 0
                },
                {
                    "studentId": 93057390,
                    "name": "PASUNURI POOJA",
                    "status": -1,
                    "remarks": "",
                    "user_status": 0,
                    "user_status_time": -1,
                    "user_rating": 0,
                    "user_comments": "",
                    "parent_id": 0,
                    "parent_name": "",
                    "parent_status": 0,
                    "parent_status_time": -1,
                    "parent_rating": 0,
                    "parent_comments": "",
                    "img_url": "",
                    "user_state": 1,
                    "contact_number": "9182798479",
                    "reg_id": "25678",
                    "p_img_url": "",
                    "org_status": 2,
                    "email": "poojareddypasunuri@gmail.com",
                    "learner_status": 1,
                    "is_nonmandatory_session": 0
                },
                {
                    "studentId": 93202873,
                    "name": "Praneesha Reddy",
                    "status": -1,
                    "remarks": "",
                    "user_status": 0,
                    "user_status_time": -1,
                    "user_rating": 0,
                    "user_comments": "",
                    "parent_id": 0,
                    "parent_name": "",
                    "parent_status": 0,
                    "parent_status_time": -1,
                    "parent_rating": 0,
                    "parent_comments": "",
                    "img_url": "",
                    "user_state": 1,
                    "contact_number": "8019736768",
                    "reg_id": "26101",
                    "p_img_url": "",
                    "org_status": 2,
                    "email": "praneeshareddy11@gmail.com",
                    "learner_status": 1,
                    "is_nonmandatory_session": 0
                },
                {
                    "studentId": 93202612,
                    "name": "Rithwik Reddy",
                    "status": 1,
                    "remarks": "",
                    "user_status": 1,
                    "user_status_time": 1784692938,
                    "user_rating": 0,
                    "user_comments": "",
                    "parent_id": 0,
                    "parent_name": "",
                    "parent_status": 0,
                    "parent_status_time": 0,
                    "parent_rating": 0,
                    "parent_comments": "",
                    "img_url": "",
                    "user_state": 1,
                    "contact_number": "9618896769",
                    "reg_id": "26100",
                    "p_img_url": "",
                    "org_status": 2,
                    "email": "rithwikreddy6769@gmail.com",
                    "learner_status": 1,
                    "is_nonmandatory_session": 0
                },
                {
                    "studentId": 93127886,
                    "name": "Varshith Poonati",
                    "status": 1,
                    "remarks": "",
                    "user_status": 1,
                    "user_status_time": 1784692979,
                    "user_rating": 0,
                    "user_comments": "",
                    "parent_id": 0,
                    "parent_name": "",
                    "parent_status": 0,
                    "parent_status_time": 0,
                    "parent_rating": 0,
                    "parent_comments": "",
                    "img_url": "",
                    "user_state": 1,
                    "contact_number": "9154332525",
                    "reg_id": "25908",
                    "p_img_url": "",
                    "org_status": 2,
                    "email": "varshithpunati000@gmail.com",
                    "learner_status": 1,
                    "is_nonmandatory_session": 0
                }
            ],
            "not_marked": 4,
            "class_type": 3,
            "topics_taught": "",
            "pages_taught": "",
            "homework": "",
            "topics_taught_ids": "",
            "signout_at": 0,
            "signout_by": 93018912,
            "signout_by_name": "Kasi Yedumati",
            "teacher_class_date": 1784658600,
            "teacher_start_time": 570,
            "teacher_end_time": 660,
            "signout_status": 0,
            "is_live": 2,
            "zoom_room_waiting": 0,
            "master_batch_id": 215863,
            "master_batch_name": "Python Full Stack Developer  with Generative AI",
            "individual_batch_attendance": 0,
            "external_class_link": "",
            "virtual_class_type": 1,
            "is_free_enrolment": 0,
            "master_batches": [
                {
                    "master_batch_id": "215863",
                    "master_batch_name": "Python Full Stack Developer  with Generative AI"
                }
            ],
            "is_sharable_link_enabled": False,
            "can_join_without_login": False,
            "joining_link": None,
            "feedback_form_id": "66b4bd9b3c7ba1df450f6254",
            "is_woolf_session": False,
            "organization_id": 6813,
            "woolf_resource_id": None,
            "is_nonmandatory_session": 0
        }
    }
}

print(students_info.get("message"))
print(students_info.get("payload", {}).get("attendance", {}).get("taken_by_name"))
print(students_info.get("payload", {}).get("attendance", {}).get("total_students", 0))
print(students_info.get("payload").get("attendance").get("student_data")[0]) # shreyas object -> i.e first student info object
print(students_info.get("payload").get("attendance").get("student_data")[0].get("name"))

# write a program to print present students and absent students
#Step1:  to get all students first
student_data = students_info.get("payload").get("attendance").get("student_data")
# iterate over every student and check his status
absent_list = []
present_list = []
for student in student_data:
    if student.get("status") == 1:
       present_list.append(student.get("name"))
    else:
        absent_list.append(student.get("name"))

print(absent_list)
print(present_list)








