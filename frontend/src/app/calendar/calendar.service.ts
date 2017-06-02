/**
 * Created by ruhi on 02/06/17.
 */
import { Injectable } from '@angular/core';
import { Http, Response, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';
import { CalendarEvent } from './calendar.event';


@Injectable()
export class CalendarService {
    private calendarUrl = 'http://localhost:8000/events/';  // URL to web API
    constructor(private http: Http) {
    }

    getEvents(): Observable<CalendarEvent[]> {
        return this.http.get(this.calendarUrl)
            .map(this.extractData)
            .catch(this.handleError);
    }

    create(title: string,
           start: Date,
           end: Date,
           isDraggable: boolean,
           isResizable: boolean): Observable<CalendarEvent> {
        let headers = new Headers({ 'Content-Type': 'application/json' });
        let options = new RequestOptions({ headers: headers });
        return this.http.post(this.calendarUrl, { title, start, end,  }, options)
            .map(this.extractData)
            .catch(this.handleError);
    }

    private extractData(res: Response) {
        let body = res.json();
        return body.data || {};
    }

    private handleError(error: Response | any) {
        // TODO: do actual error handling
        return Observable.throw("Database failed");
    }
}
