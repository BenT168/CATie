import {Component, Injectable, OnInit} from '@angular/core';
import {CoursesService} from "../_services/courses.service";
import {Router} from '@angular/router';
import {AuthenticationService} from "../_services/auth.service";

interface LectureDictionary {
    [key: number]: Lecture[];
}

@Component({
    styleUrls: ['./courses.component.scss'],
    templateUrl: './courses.component.html'
})

export class CoursesComponent implements OnInit {
    lecturesLoaded: boolean;
    model: any = {};
    allExpanded: boolean;
    isStaff: boolean;
    viewStaffModal: boolean;
    viewStudentModal: boolean;
    viewStudentWithdrawnModal: boolean;
    firstName: string;
    lastName: string;
    _ref : any;

    courses: Course[] = [];
    enrolledCourses: Course[] = [];
    lectureDict: LectureDictionary = {};

    localStorage;

    constructor(private coursesService: CoursesService, private router: Router, private authenticationService: AuthenticationService) {
        this.allExpanded = false;
        this.viewStaffModal = false;
        this.viewStudentModal = false;
        this.viewStudentWithdrawnModal = false;
        this.localStorage = localStorage;
        this.isStaff = JSON.parse(localStorage['currentUser']).is_staff;
        this.firstName = JSON.parse(localStorage['currentUser']).first_name;
        this.lastName = JSON.parse(localStorage['currentUser']).last_name;
        console.log(this.isStaff);
        this.lecturesLoaded = false;
    }

    logout(): void {
        this.authenticationService.logout();
    }

    expandButtonPress() {
        this.allExpanded = !this.allExpanded;
    }

    showStaffModal() {
        this.viewStaffModal = true;
    }

    hideStaffModal() {
        this.viewStaffModal = false;
    }

    showStudentWithdrawnModal() {
        this.viewStudentWithdrawnModal = true;
    }

    hideStudentWithdrawnModal() {
        this.viewStudentWithdrawnModal = false;
    }

    showStudentModal() {
        this.viewStudentModal = true;
    }

    hideStudentModal() {
        this.viewStudentModal = false;
    }

    getAllLectures() {
        if (!this.lecturesLoaded) {
            if (this.isStaff) {
                for (let course of this.courses) {
                    this.getLectures(course.code);
                }
            } else {
                for (let course of this.courses) {
                    this.getLectures(course.code);
                }
            }
            this.lecturesLoaded = true;
        }
    }

    ngOnInit() {
        this.getCourses();
    }

    getCourses() {
        this.coursesService.getCourses().subscribe(
            courses => this.courses = courses,
            function(error) { console.log(error); },
            function() { console.log("completed course loading"); }
        );
    }

    getEnrolledCourses() {
        this.coursesService.getEnrolledCourses().subscribe(
            enrolledCourses => this.enrolledCourses = enrolledCourses,
            function(error) { console.log(error); },
            function() { console.log("enrolled course loading"); }
        );
    }

    getLectures(code: number) {
        this.coursesService.getLectures(code).subscribe(
            lectures => this.lectureDict[code] = lectures,
            function(error) { console.log(error); },
            function() { console.log("completed lecture loading for " + code); }
        );
    }

    addSession() {
        let status = this.coursesService.addSession(this.model.name, this.model.course.split(":", 1)[0],
                     this.model.video, this.model.slides).subscribe(result => {
            console.log(result);
        });
        console.log("status on courses page:");
        console.log(status);
        this.hideStaffModal();
    }

    addCourse() {
        let status = this.coursesService.addCourse(this.model.name, this.model.course.split(":", 1)[0]).subscribe(result => {
            console.log(result);
        });
        console.log("status on courses page:");
        console.log(status);
        this.hideStudentModal();
    }

     deleteCourse() {
        this._ref.destroy();
        let status = this.coursesService.deleteCourse(this.model.name, this.model.course.split(":", 1)[0]).subscribe(result => {
            console.log(result);
        });
        console.log("status on courses page:");
        console.log(status);
        this.hideStudentWithdrawnModal();
    }
}

export class Course {
    constructor(
        public code: number,
        public name: string) { }
}

export class Lecture {
    urlNameWithCode: string;
    constructor(
        public name: string,
        public urlName: string) { }
}
