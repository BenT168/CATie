import {Component} from '@angular/core';
import {Router} from '@angular/router';
import {AuthenticationService} from "../_services/auth.service";

@Component({
    styleUrls: ['./grades.component.scss'],
    templateUrl: './grades.component.html'
})

export class GradesComponent {
    isStaff: boolean;
    allExpanded: boolean;
    showFeedback: boolean;

    constructor(private router: Router, private authenticationService: AuthenticationService) {
        this.allExpanded = false;
        this.showFeedback = false;
        this.isStaff = JSON.parse(localStorage['currentUser']).is_staff;
    }

    expandButtonPress() {
        this.allExpanded = !this.allExpanded;
    }

    showFeedbackModal() {
        this.showFeedback = true;
    }

    hideFeedbackModal() {
        this.showFeedback = false;
    }

    logout(): void {
        this.authenticationService.logout();
    }
}
