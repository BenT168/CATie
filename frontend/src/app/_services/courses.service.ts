import { Injectable } from '@angular/core';
import {Http, Headers, Response, RequestOptions} from '@angular/http';
import { Observable } from "rxjs/Observable";
import 'rxjs/add/operator/map';
import * as Globals from '../globals';

import {Course, Lecture} from '../courses/courses.component';
import {LectureDetails} from "../catieviewer/catieviewer.component";

@Injectable()
export class CoursesService {
    public token: string;
    private fetchCoursesUrl: string = Globals.hostURL + 'courses/';
    private addUrl: string = Globals.hostURL + 'lectures/create/';
    private courseData = [
                        {"code":303,"name":"Systems Verification"},
                        {"code":304,"name":"Logic-Based Learning"},
                        {"code":316,"name":"Computer Vision"},
                        {"code":317,"name":"Graphics"},
                        {"code":318,"name":"Custom Computing"},
                        {"code":322,"name":"Communicating Computer Science in Schools"},
                        {"code":331,"name":"Network and Web Security"},
                        {"code":332,"name":"Advanced Computer Architecture"},
                        {"code":333,"name":"Robotics"},
                        {"code":337,"name":"Simulation and Modelling"},
                        {"code":338,"name":"Pervasive Computing"},
                        {"code":343,"name":"Operations Research"},
                        {"code":347,"name":"Distributed Algorithms"},
                        {"code":349,"name":"Information and Coding Theory"},
                        {"code":382,"name":"Type Systems for Programming Languages"},
                        {"code":395,"name":"Machine Learning"},
                        {"code":572,"name":"Advanced Databases"}]

    public lectureData = [{
            "code": 337, "lectures": [{
                "name": "Introduction to Simulation and Modelling",
                "urlNameWithCode": "337/introduction-simul",
                "urlName": "introduction-simul",
                "video": "https://imperial.cloud.panopto.eu/Panopto/Pages/Embed.aspx?id=df19de61-a458-49c8-ba48-e5aa611f7773",
                "slides": "http://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf",
                "notes": "",
                "questions": [{
                    "id": 1,
                    "title": "PS4 Q3, where do i find the example?",
                    "body": "Sample body - add in text later"
                }]
            }]
        }
    ]

    constructor(private http: Http) {
        // set token if saved in local storage
        let currentUser = JSON.parse(localStorage.getItem('currentUser'));
        this.token = currentUser && currentUser.token;
    }

    getCourses(): Observable<Course[]> {
        //let headers = new Headers();
        //headers.append('Authorization', this.token);
        //let options = new RequestOptions({ headers: headers });
        //return this.http.get(this.fetchCoursesUrl, options).map(this.extractData);
        return Observable.of(this.courseData);
    }

    getLectures(code: number): Observable<Lecture[]> {
        //let headers = new Headers();
        //headers.append('Authorization', this.token);
        //let options = new RequestOptions({ headers: headers });
        //let url = this.fetchCoursesUrl + code + '/';
        //return this.http.get(url, options).map(this.extractData);
        for (let course of this.lectureData) {
            if (course.code == code) {
                return Observable.of(course.lectures);
            }
        }
        return Observable.of([]);
    }

    addSession(name: string, code: string, video: string, slides: string): Observable<number>  {
        let headers = new Headers({'Content-Type': 'application/x-www-form-urlencoded'});
        headers.append('Authorization', this.token);
        let options = new RequestOptions({ headers: headers });
        let body = 'name=' + name + '&code=' + code + '&video=' + video + '&slides=' + slides;

        return this.http.post(this.addUrl, body, options).map((res: Response) => {
            if (res) {
                return res.status;
            }
        });
    }

    saveNotes(content: string, code: number, urlName: string) {
        let headers = new Headers({'Content-Type': 'application/x-www-form-urlencoded'});
        headers.append('Authorization', this.token);
        let options = new RequestOptions({ headers: headers});
        let body = 'content=' + content;

        return this.http.post(this.fetchCoursesUrl + code + '/' + urlName + '/save/', body, options).map((res: Response) => {
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

    getUrls(urlNameWithCode: string): Observable<LectureDetails> {
        //let headers = new Headers();
        //headers.append('Authorization', this.token);
        //let options = new RequestOptions({ headers: headers });
        //let url = this.fetchCoursesUrl + urlname + '/';
        //return this.http.get(url, options).map(this.extractData);
        for (let course of this.lectureData) {
            for (let lecture of course.lectures) {
                if (lecture.urlNameWithCode == urlNameWithCode) {
                    return Observable.of({
                        "name": lecture.name,
                        "slides": lecture.slides,
                        "video": lecture.video,
                        "notes": lecture.notes
                    });
                }
            }
        }
        return Observable.of({});
    }
}

// /save/
