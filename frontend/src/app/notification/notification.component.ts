import {Component, Injectable, OnInit, OnDestroy} from '@angular/core';
import {NotificationService} from "../_services/notification.service";
import {ActivatedRoute,Router} from '@angular/router';
import {AuthenticationService} from "../_services/auth.service";
import {FormBuilder} from '@angular/forms';
import {Course} from '../courses/courses.component';
import {CoursesService} from "../_services/courses.service";
import {Subscription} from "rxjs/Subscription";

@Component({
    styleUrls: ['./notification.component.scss'],
    templateUrl: './notification.component.html'
})

export class NotificationComponent implements OnInit, OnDestroy {
    model: any = {};
    allExpanded: boolean;
    isStaff: boolean;
    viewStaffModal: boolean;
    viewNotificationModal: boolean;
    firstName: string;
    lastName: string;
    message: string;
    course: number;
    category: string;

    notification: Notification[] = [];

    notificationSubscription: Subscription;
    selectedCourse: Course = null;

    localStorage;

    constructor(private notificationService: NotificationService, private router: Router, private authenticationService: AuthenticationService, course: number, message: string, category: string) {
        this.allExpanded = false;
        this.viewStaffModal = false;
        this.viewNotificationModal = false;
        this.localStorage = localStorage;
        this.isStaff = JSON.parse(localStorage['currentUser']).is_staff;
        this.firstName = JSON.parse(localStorage['currentUser']).first_name;
        this.lastName = JSON.parse(localStorage['currentUser']).last_name;
        this.course = course;
        this.message = message;
        this.category = category;
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

    showNotificationModal() {
        this.viewNotificationModal = true;
    }

    hideQNotificationModal() {
        this.viewNotificationModal = false;
    }

    ngOnInit() {
        this.getNotification();
    }

    ngOnDestroy() {
        if (this.notificationSubscription !== undefined) {
            this.notificationSubscription.unsubscribe();
        }
    }

    getNotification() {
        this.notificationService.getNotification().subscribe(
            notification => this.notification = notification,
            function(error) { console.log(error); },
            function() { console.log("all notifications loaded"); }
        );
    }

    createNotification() {
        this.notificationService.createNotification(this.model.title, this.selectedCourse.code,
            this.model.body,this.model.category).subscribe(result => {
            console.log(result);
        });
    }

  }
