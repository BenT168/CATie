import {Component} from '@angular/core';
import {Router} from '@angular/router';
import {AuthenticationService} from "../_services/auth.service";

@Component({
    styleUrls: ['./assignments.component.scss'],
    templateUrl: './assignments.component.html'
})

export class AssignmentsComponent {
    isStaff: boolean;
    showSubmission: boolean;
    showMoreInfo: boolean;
    submissionValue: number;
    submitLoading: boolean;

    constructor(private router: Router, private authenticationService: AuthenticationService) {
        this.showSubmission = false;
        this.showMoreInfo = false;
        this.submissionValue = 0;
        this.submitLoading = false;
        this.isStaff = JSON.parse(localStorage['currentUser']).is_staff;
    }

    logout(): void {
        this.authenticationService.logout();
    }

    showSubmissionModal() {
        this.showSubmission = true;
    }

    hideSubmissionModal() {
        this.showSubmission = false;
    }

    showMoreInfoModal() {
        this.showMoreInfo = true;
    }

    hideMoreInfoModal() {
        this.showMoreInfo = false;
    }

    submit() {
        this.submissionValue = 100;
        this.submitLoading = true;
    }
}
