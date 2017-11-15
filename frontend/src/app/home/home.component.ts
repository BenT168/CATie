/*
 * Copyright (c) 2016 VMware, Inc. All Rights Reserved.
 * This software is released under MIT license.
 * The full license information can be found in LICENSE in the root directory of this project.
 */
import {Component} from "@angular/core";
import {Router} from '@angular/router';
import {AuthenticationService} from "../_services/auth.service";
import {AskAriService} from "../_services/askari.service";
import {Question} from "../askari/askari.component";
import {NotificationService} from "../_services/notification.service"
import {NotificationComponent} from "../notification/notification.component";

@Component({
    styleUrls: ['./home.component.scss'],
    templateUrl: './home.component.html',
})
export class HomeComponent {
    isStaff: boolean;
    firstName: string;
    lastName: string;
    questions: Question[];
    notification: NotificationComponent[] = [];

    constructor(private router: Router, private authenticationService: AuthenticationService,
                private askAriService: AskAriService, private notificationService: NotificationService) {
        this.isStaff = JSON.parse(localStorage['currentUser']).is_staff;
        this.firstName = JSON.parse(localStorage['currentUser']).first_name;
        this.lastName = JSON.parse(localStorage['currentUser']).last_name;
        this.loadQuestions();
        // this.getNotification()
        this.createNots(notificationService, router, authenticationService);
    }

    logout(): void {
        this.authenticationService.logout();
    }

    loadQuestions() {
        this.askAriService.getAllQuestions().subscribe(
            questions => this.questions = questions,
            function(error) { console.log(error); },
            function() { console.log("got all questions"); }
        );
    }

    // getNotification() {
    //     this.notificationService.getNotification().subscribe(
    //         notification => this.notification = notification,
    //         function(error) { console.log(error); },
    //         function() { console.log("all notifications loaded"); }
    //     );
    // }

    createNots(notificationService: NotificationService, router: Router, authenticationService: AuthenticationService): void {
      this.notification.push(new NotificationComponent(notificationService, router, authenticationService, 290, "Grade Release", "done"));
      this.notification.push(new NotificationComponent(notificationService, router, authenticationService, 209, "New Assignment Available", "note"));
      this.notification.push(new NotificationComponent(notificationService, router, authenticationService, 256, "New tutorial available", "note"));
      this. notification.push(new NotificationComponent(notificationService, router, authenticationService, 235, "Latest lecture released", "note"));
      this.notification.push(new NotificationComponent(notificationService, router, authenticationService, 235, "Upcoming Deadline", "clock"));
      this.notification.push(new NotificationComponent(notificationService, router, authenticationService, 217, "New assignment available", "note"));
      this.notification.push(new NotificationComponent(notificationService, router, authenticationService, 289, "Response to your Ask ARi Question", "discussion"));
      this.notification.push(new NotificationComponent(notificationService, router, authenticationService, 290, "Assignment Submission Successful", "upload-success"));
      this.notification.push(new NotificationComponent(notificationService, router, authenticationService, 234, "Assignment Submission Failed", "upload-failure"));
    }

    deleteNots(not: NotificationComponent): void {
      const index: number = this.notification.indexOf(not);
      if (index !== -1) {
        this.notification.splice(index, 1);
    }
    }
}
