import { Injectable } from '@angular/core';
import { Http, Response, RequestOptions, Headers } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';
import { CalendarEvent } from './calendar.event';
import * as Globals from '../globals';


@Injectable()
export class CalendarService {
    public token: string;

    private calendarUrl: string = Globals.hostURL + 'calendar/';  // URL to web API
    private createEventUrl: string = Globals.hostURL + 'calender/create/';

    constructor(private http: Http) {
        let currentUser = JSON.parse(localStorage.getItem('currentUser'));
        this.token = currentUser && currentUser.token;
    }

    getEvents(): Observable<CalendarEvent[]> {
        return this.http.get(this.calendarUrl)
            .map(this.extractData)
            .catch(this.handleError);
    }

    create(username: string,
           password: string,
           title: string,
           start: Date,
           end: Date,
           content: string,
           isDraggable: boolean,
           isResizable: boolean): Observable<CalendarEvent> {
        let headers = new Headers({ 'Content-Type': 'application/json' });
        headers.append('Authorization', this.token);
        let options = new RequestOptions({ headers: headers });
        return this.http.post(this.createEventUrl, { username, title, start, end, content, isDraggable, isResizable  }, options)
            .map(this.extractData)
            .catch(this.handleError);
    }

    // TODO: create a CalendarEvent object from this method?
    private extractData(res: Response) {
        let body = res.json();
        return body.data || {}; // .data because JSON is wrapped by an object
    }

    private handleError(error: Response | any) {
        // TODO: do actual error handling
        return Observable.throw("Database failed.");
    }
}
