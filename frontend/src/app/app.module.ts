import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule, JsonpModule } from '@angular/http';
import { ClarityModule } from 'clarity-angular';
import { AppComponent } from './app.component';
import { ROUTING } from "./app.routing";
import { HomeComponent } from "./home/home.component";
import { AboutComponent } from "./about/about.component";
import { CalendarModule } from 'angular-calendar';

import { NotificationComponent } from './notification/notification.component';
import { CalendarComponent } from './calendar/calendar.component';
import { CoursesComponent } from "./courses/courses.component";
import { GradesComponent } from "./grades/grades.component";
import { CATieViewerComponent, SafePipe } from "./catieviewer/catieviewer.component";
import { AskCATieComponent } from "./askcatie/askcatie.component";
import { LoginComponent } from "./login/login.component";
import { AskCATieQuestionComponent } from "./askcatiequestion/askcatiequestion.component";
import { AssignmentsComponent } from "./assignments/assignments.component";
import { GradingSchemaComponent } from "./gradingschema/gradingschema.component";
import { DocCalendarComponent } from "./doccalendar/doccalendar.component";
import { AuthGuard } from "./_guards/auth.guard";
import { LoginGuard } from "./_guards/login.guard";
import { AuthenticationService } from "./_services/auth.service";
import { CoursesService } from "./_services/courses.service";
import { AskCATieService } from "./_services/askcatie.service";
import { NotificationService } from "./_services/notification.service";

@NgModule({
    declarations: [
        AppComponent,
        AboutComponent,
        HomeComponent,
        CalendarComponent,
        CoursesComponent,
        NotificationComponent,
        GradesComponent,
        CATieViewerComponent,
        LoginComponent,
        AskCATieComponent,
        AskCATieQuestionComponent,
        AssignmentsComponent,
        GradingSchemaComponent,
        DocCalendarComponent,
        SafePipe
    ],
    imports: [
        BrowserAnimationsModule,
        BrowserModule,
        FormsModule,
        HttpModule,
        JsonpModule,
        ClarityModule.forRoot(),
        CalendarModule.forRoot(),
        ROUTING,
        ReactiveFormsModule
    ],
    providers: [
        AuthGuard,
        LoginGuard,
        AuthenticationService,
        CoursesService,
        NotificationService,
        AskCATieService
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
}
