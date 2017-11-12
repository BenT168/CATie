import { Injectable } from '@angular/core';
import {Http, Headers, Response, RequestOptions} from '@angular/http';
import { Observable } from "rxjs/Observable";
import 'rxjs/add/operator/map';
import * as Globals from '../globals';

import {LectureDetails} from "../ariviewer/ariviewer.component";
import {NotificationComponent} from "../notification/notification.component";

@Injectable()
export class NotificationService {
    public token: string;

    private fetchNotificationUrl: string = Globals.hostURL + 'notification/';
    private createNotificationUrl: string = Globals.hostURL + 'notification/create/';

    constructor(private http: Http) {
        // set token if saved in local storage
        let currentUser = JSON.parse(localStorage.getItem('currentUser'));
        this.token = currentUser && currentUser.token;
    }

    getNotification(): Observable<Notification[]> {
        let headers = new Headers();
        headers.append('Authorization', this.token);
        let options = new RequestOptions({ headers: headers });
        return this.http.get(this.fetchNotificationUrl, options).map(this.extractData);
    }

    createNotification(title: string, code: number, body: string, category: string): Observable<number>  {
        let headers = new Headers({'Content-Type': 'application/x-www-form-urlencoded'});
        headers.append('Authorization', this.token);
        let options = new RequestOptions({ headers: headers });
        let params = 'title=' + title + '&code=' + code + '&body=' + body +'&category=' + category ;

        return this.http.post(this.createNotificationUrl, params, options).map((res: Response) => {
            if (res) {
                return res.status;
            }
        });
    }

    private extractData(res: Response) {
        let body = res.json();
        console.log('ExtractData: ' + body);
        return body || [];
    }

    getUrls(urlname: string): Observable<LectureDetails> {
        let headers = new Headers();
        headers.append('Authorization', this.token);
        let options = new RequestOptions({ headers: headers });
        let url = this.fetchNotificationUrl + urlname + '/';
        return this.http.get(url, options).map(this.extractData);
    }
}

// /save/
