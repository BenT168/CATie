/*
 * Copyright (c) 2016 VMware, Inc. All Rights Reserved.
 * This software is released under MIT license.
 * The full license information can be found in LICENSE in the root directory of this project.
 */
import { ModuleWithProviders } from '@angular/core/src/metadata/ng_module';
import { Routes, RouterModule } from '@angular/router';

import { AboutComponent } from './about/about.component';
import { HomeComponent } from './home/home.component';
import { CalendarComponent } from "./calendar/calendar.component";
import { NotificationComponent } from "./notification/notification.component";
import { CoursesComponent } from "./courses/courses.component";
import { GradesComponent } from "./grades/grades.component";
import { CATieViewerComponent } from "./catieviewer/catieviewer.component";
import { AskCATieComponent } from "./askcatie/askcatie.component";
import { AssignmentsComponent } from "./assignments/assignments.component";
import { GradingSchemaComponent } from "./gradingschema/gradingschema.component";
import { DocCalendarComponent } from "./doccalendar/doccalendar.component";
import { LoginGuard } from "./_guards/login.guard";
import { AuthGuard } from "./_guards/auth.guard";
import { LoginComponent } from "./login/login.component";
import { AskCATieQuestionComponent } from "./askcatiequestion/askcatiequestion.component";

export const ROUTES: Routes = [
    { path: '', redirectTo: 'home', pathMatch: 'full' },
    { path: 'login', component: LoginComponent, canActivate: [LoginGuard]},
    { path: 'home', component: HomeComponent, canActivate: [AuthGuard] },
    { path: 'about', component: AboutComponent, canActivate: [AuthGuard] },
    { path: 'notification', component: NotificationComponent, canActivate: [AuthGuard] },
    { path: 'cal', component: CalendarComponent, canActivate: [false] },
    { path: 'courses', component: CoursesComponent, canActivate: [AuthGuard] },
    { path: 'grades', component: GradesComponent, canActivate: [AuthGuard] },
    { path: 'catieviewer', component: CATieViewerComponent, canActivate: [AuthGuard] },
    { path: 'catieviewer/:courseCode/:lectureName', component: CATieViewerComponent, canActivate: [AuthGuard] },
    { path: 'askcatie', component: AskCATieComponent, canActivate: [AuthGuard] },
    { path: 'assignments', component: AssignmentsComponent, canActivate: [AuthGuard] },
    { path: 'gradingschema', component: GradingSchemaComponent, canActivate: [AuthGuard] },
    { path: 'doccalendar', component: DocCalendarComponent, canActivate: [AuthGuard] },
    { path: 'askcatiequestion', component: AskCATieQuestionComponent, canActivate: [AuthGuard] }
];

export const ROUTING: ModuleWithProviders = RouterModule.forRoot(ROUTES);
