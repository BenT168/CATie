/*
 * Copyright (c) 2016 VMware, Inc. All Rights Reserved.
 * This software is released under MIT license.
 * The full license information can be found in LICENSE in the root directory of this project.
 */
import {Component, OnInit} from '@angular/core';
import {CalendarService} from "./calendar.service";
import {CalendarEvent} from "./calendar.event";
import {Router} from '@angular/router';
import {AuthenticationService} from "../_services/auth.service";

@Component({
    styleUrls: ['./about.component.scss'],
    templateUrl: './about.component.html',
    providers: [ CalendarService ]
})
export class AboutComponent implements OnInit {
    errorMessage: string;
    events: CalendarEvent[];
    mode = 'Observable';
    isStaff: boolean;

    constructor (private calendarService: CalendarService, private router: Router, private authenticationService: AuthenticationService) {
        this.isStaff = JSON.parse(localStorage['currentUser']).is_staff;
    }

    logout(): void {
        this.authenticationService.logout();
    }

    ngOnInit() { this.getEvents(); }

    getEvents() {
        this.calendarService.getEvents()
            .subscribe(
                events => this.events = events,
                error =>  this.errorMessage = <any>error);
    }

    addEvent(username: string, title: string, start: Date, end: Date, isDraggable: boolean, isResizable: boolean) {
        if (!name) { return; }
        this.calendarService.create(username, title, start, end, isDraggable, isResizable)
            .subscribe(
                hero  => this.events.push(hero),
                error =>  this.errorMessage = <any>error);
    }
}
