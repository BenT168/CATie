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
                        {"code":120.1,"name":"Programming I"},
                        {"code":161,"name":"Laboratory"},
                        {"code":316,"name":"Computer Vision"},
                        {"code":317,"name":"Graphics"},
                        {"code":572,"name":"Advanced Databases"},
                        {"code":318,"name":"Custom Computing"},
                        {"code":322,"name":"Communicating Computer Science in Schools"},
                        {"code":331,"name":"Network and Web Security"},
                        {"code":332,"name":"Advanced Computer Architecture"},
                        {"code":333,"name":"Robotics"},
                        {"code":337,"name":"Simulation and Modelling"},
                        {"code":191,"name":"Advanced Programming"},
                        {"code":343,"name":"Operations Research"},
                        {"code":347,"name":"Distributed Algorithms"},
                        {"code":349,"name":"Information and Coding Theory"},
                        {"code":382,"name":"Type Systems for Programming Languages"},
                        {"code":395,"name":"Machine Learning"}]
//
//                         // {"code":316,"name":"Computer Vision"},
//                         // {"code":317,"name":"Graphics"},
//                         // {"code":318,"name":"Custom Computing"},
//                         // {"code":322,"name":"Communicating Computer Science in Schools"},
//                         // {"code":331,"name":"Network and Web Security"},
//                         // {"code":332,"name":"Advanced Computer Architecture"},
//                         // {"code":333,"name":"Robotics"},
//                         {"code":337,"name":"Simulation and Modelling"}]
//                         // {"code":191,"name":"Advanced Programming"},
//                         // {"code":343,"name":"Operations Research"},
//                         // {"code":347,"name":"Distributed Algorithms"},
//                         // {"code":349,"name":"Information and Coding Theory"},
//                         // {"code":382,"name":"Type Systems for Programming Languages"},
//                         // {"code":395,"name":"Machine Learning"},
//                         // {"code":572,"name":"Advanced Databases"}]
//
    private enrolledCourseData = [
                        {"code":316,"name":"Computer Vision"},
                        {"code":317,"name":"Graphics"},
                        {"code":331,"name":"Network and Web Security"},
                        {"code":333,"name":"Robotics"},
                        {"code":337,"name":"Simulation and Modelling"},
                        {"code":347,"name":"Distributed Algorithms"},
                        {"code":395,"name":"Machine Learning"}]
//
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
                    "body": "Sample body add in text later"
                }, {
                    "id": 2,
                    "title": "Trapezoidal Density function",
                    "body": "Can anyone help me derive a density function for a trapezoidal graph as described in question 2 in the 2015 paper?"
                }]
            }]
        }, {
            "code": 572, "lectures": [{
                "name": "Advanced Databases - Temporal Databases",
                "urlNameWithCode": "572/temporal-databases",
                "urlName": "temporal-databases",
                "video": "https://imperial.cloud.panopto.eu/Panopto/Pages/Embed.aspx?id=3bba2df7-8655-45cd-a4b1-f46aff444d9c",
                "slides": "http://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf",
                "notes": "",
                "questions": [{
                    "id": 1,
                    "title": "Does the order of temporal database query result matters?",
                    "body": "in the exam, are we are expected to write the querying result in a correct order?"
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

    getEnrolledCourses(): Observable<Course[]> {
        //let headers = new Headers();
        //headers.append('Authorization', this.token);
        //let options = new RequestOptions({ headers: headers });
        //return this.http.get(this.fetchCoursesUrl, options).map(this.extractData);
        return Observable.of(this.enrolledCourseData);
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

    addCourse(name: string, code: string): Observable<number>  {
        let headers = new Headers({'Content-Type': 'application/x-www-form-urlencoded'});
        headers.append('Authorization', this.token);
        let options = new RequestOptions({ headers: headers });
        let body = 'name=' + name + '&code=' + code;

        return this.http.post(this.addUrl, body, options).map((res: Response) => {
            if (res) {
                return res.status;
            }
        });
    }

    deleteCourse(name: string, code: string): Observable<number>  {
        let headers = new Headers({'Content-Type': 'application/x-www-form-urlencoded'});
        headers.append('Authorization', this.token);
        let options = new RequestOptions({ headers: headers });
        let body = 'name=' + name + '&code=' + code;

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
