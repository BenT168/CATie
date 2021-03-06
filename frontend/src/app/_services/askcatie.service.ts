import {Injectable} from '@angular/core';
import {Http, Headers, Response, RequestOptions} from '@angular/http';
import {Observable} from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import * as Globals from '../globals';
import {CoursesService} from "../_services/courses.service";

import {LectureDetails} from "../catieviewer/catieviewer.component";
import {Question} from "../askcatie/askcatie.component";

@Injectable()
export class AskCATieService {
    public token: string;

    private allQuestionsUrl: string = Globals.hostURL + 'AskCATie/';
    private allQuestionsByPageUrl: string = Globals.hostURL + 'AskCATie/#page_number'; // page_number is a variable
    private allQuestionsByCourseUrl: string = Globals.hostURL + 'AskCATie/course_number'; // course_number is a variable
    private allQuestionsByCourseAndPageUrl: string = Globals.hostURL + 'AskCATie/course_number/#page_number'; // course_number and page_number are variables
    private allQuestionsByCourseAndLectureUrl: string = Globals.hostURL + 'AskCATie/course_number/lecture_name'; // course_number and lecture_name are variables
    private allQuestionsByCourseAndLectureAndPageUrl: string = Globals.hostURL + 'AskCATie/course_number/lecture_name/#page_number'; // course_number, page_number and lecture_name are variables

    private questionAndCommentsUrl: string = Globals.hostURL + 'AskCATie/question/';
    private addCommentUrl: string = Globals.hostURL + 'AskCATie/question/'; // question/'code'/'urlname'/'questionid'/reply/

    private createQuestionUrl: string = Globals.hostURL + 'AskCATie/question/create/';

    constructor(private http: Http, private coursesService: CoursesService) {
        // set token if saved in local storage
        let currentUser = JSON.parse(localStorage.getItem('currentUser'));
        this.token = currentUser && currentUser.token;
    }

    getAllQuestions(): Observable<Question[]> {
        //let headers = new Headers();
        //headers.append('Authorization', this.token);
        //let options = new RequestOptions({ headers: headers });
        //return this.http.get(this.allQuestionsUrl, options).map(this.extractData);
        var questions = [];
        for (let course of this.coursesService.lectureData) {
            for (let lecture of course.lectures) {
                questions = questions.concat(lecture.questions);
            }
        }
        return Observable.of(questions);
    }

    getQuestionsForCourse(courseCode: number): Observable<Question[]> {
        //let headers = new Headers();
        //headers.append('Authorization', this.token);
        //let options = new RequestOptions({ headers: headers });
        //return this.http.get(this.allQuestionsUrl + String(courseCode) + '/', options).map(this.extractData);
        var questions = [];
        for (let course of this.coursesService.lectureData) {
            if (course.code == courseCode) {
                for (let lecture of course.lectures) {
                    questions = questions.concat(lecture.questions);
                }
            }
        }
        return Observable.of(questions);
    }

    getQuestionsForCourseAndLecture(courseCode: number, lectureUrl: string): Observable<Question[]> {
        //let headers = new Headers();
        //headers.append('Authorization', this.token);
        //let options = new RequestOptions({ headers: headers });
        //return this.http.get(this.allQuestionsUrl + String(courseCode) + '/' + lectureUrl + '/', options)
        //        .map(this.extractData);
        var questions = [];
        for (let course of this.coursesService.lectureData) {
            if (course.code == courseCode) {
                for (let lecture of course.lectures) {
                    if (lecture.urlName == lectureUrl) {
                        questions = questions.concat(lecture.questions);
                    }
                }
            }
        }
        return Observable.of(questions);
    }

    getQuestion(code: number, lectureUrl: string, questionID: number): Observable<Question> {
        //let headers = new Headers();
        //headers.append('Authorization', this.token);
        //let options = new RequestOptions({ headers: headers });
        //let url = this.questionAndCommentsUrl + code + '/' + lectureUrl + '/' + questionID + '/';
        //return Observable.timer(0, 2000)
        //    .switchMap(() => this.http.get(url, options).map(this.extractData));
        var questions = [];
        for (let course of this.coursesService.lectureData) {
            if (course.code == code) {
                for (let lecture of course.lectures) {
                    if (lecture.urlName == lectureUrl) {
                        for (let question of lecture.questions) {
                            if (question.id == questionID) {
                                return Observable.of(question);
                            }
                        }
                    }
                }
            }
        }
        return Observable.of({});
    }

    addComment(content: string, question: number, code: number, urlname: string) {
        let headers = new Headers({'Content-Type': 'application/x-www-form-urlencoded'});
        headers.append('Authorization', this.token);
        let options = new RequestOptions({ headers: headers });
        let body = 'content=' + content;
        console.log(body);
        let url = this.addCommentUrl + code + '/' + urlname + '/' + question + '/reply/';

        return this.http.post(url, body, options).map((res: Response) => {
            if (res) {
                return res.status;
            }
        });
    }

    addCommentReply(content: string, question: number, code: number, urlname: string, parent: number) {
        let headers = new Headers({'Content-Type': 'application/x-www-form-urlencoded'});
        headers.append('Authorization', this.token);
        let options = new RequestOptions({ headers: headers });
        let body = 'content=' + content + '&parent=' + parent;
        console.log(body);
        let url = this.addCommentUrl + code + '/' + urlname + '/' + question + '/reply/';

        return this.http.post(url, body, options).map((res: Response) => {
            if (res) {
                return res.status;
            }
        });
    }

    // This function is used to TOGGLE the upvote on a comment depending on the boolean
    upvoteComment(code: number, lecture: string, questionId: number, commentId: number, isUpvote: boolean): Observable<number> {
        let headers = new Headers({'Content-Type': 'application/x-www-form-urlencoded'});
        headers.append('Authorization', this.token);
        let options = new RequestOptions({ headers: headers });
        let rating: number = isUpvote ? 1 : 0;
        let body = 'rating=' + String(rating);

        let url = this.questionAndCommentsUrl + String(code) + '/' +
            lecture + '/' + String(questionId) + '/' + String(commentId) + '/rate/';

        return this.http.post(url, body, options).map((res: Response) => {
            if (res) {
                return res.status;
            }
        });
    }

    /*
    getAllQuestionsByPage(code: number): Observable<Lecture[]> {
        let headers = new Headers();
        headers.append('Authorization', this.token);
        let options = new RequestOptions({ headers: headers });
        let url = this.fetchCoursesUrl + code + '/';
        return this.http.get(url, options).map(this.extractData);
    }
    */

    createQuestion(title: string, code: number, lecture: string, body: string): Observable<number>  {
        //let headers = new Headers({'Content-Type': 'application/x-www-form-urlencoded'});
        //headers.append('Authorization', this.token);
        //let options = new RequestOptions({ headers: headers });
        //let params = 'title=' + title + '&code=' + code + '&lecture=' + lecture + '&body=' + body;

        //return this.http.post(this.createQuestionUrl, params, options).map((res: Response) => {
        //    if (res) {
        //        return res.status;
        //    }
        //});
        var lecData = this.coursesService.lectureData;
        var i = 0;
        var j = 0;
        var k = 0;
        for (i = 0; i < lecData.length; i++) {
            if (lecData[i].code == code) {
                for (j = 0; j < lecData[i].lectures.length; j++) {
                    if (lecData[i].lectures[j].urlName == lecture) {
                        var newQuestionID = 1;
                        for (k = 0; k < lecData[i].lectures[j].questions.length; k++) {
                            if (lecData[i].lectures[j].questions[k].id >= newQuestionID) {
                                newQuestionID = lecData[i].lectures[j].questions[k].id + 1;
                            }
                        }
                        var newQuestion = {
                            "id": newQuestionID,
                            "title": title,
                            "body": body
                        };
                        lecData[i].lectures[j].questions.concat(newQuestion);
                        this.coursesService.lectureData = lecData;
                        return Observable.of(newQuestionID);
                    }
                }
            }
        }
        return Observable.of(0);
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
        let url = this.allQuestionsUrl + urlname + '/';
        return this.http.get(url, options).map(this.extractData);
    }
}
