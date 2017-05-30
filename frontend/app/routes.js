"use strict";
var router_1 = require('@angular/router');
var home_component_1 = require('./components/home/home.component');
var reviews_component_1 = require('./components/reviews/reviews.component');
var add_component_1 = require("./components/reviews/add/add.component");
var statistic_component_1 = require("./components/reviews/statistic/statistic.component");
var authguard_1 = require("./services/authguard");
var events_component_1 = require("./components/events/events.component");
exports.routes = [
    { path: '', component: home_component_1.HomeComponent, pathMatch: 'full' },
    { path: 'reviews',
        component: reviews_component_1.ReviewComponent,
        children: [
            { path: '', component: statistic_component_1.StatisticReviewComponent },
            { path: 'add', component: add_component_1.AddReviewComponent }
        ]
    },
    { path: 'events', component: events_component_1.EventsComponent, canActivate: [authguard_1.AuthGuard] }
];
exports.APP_ROUTER_PROVIDERS = [
    authguard_1.AuthGuard,
];
exports.routing = router_1.RouterModule.forRoot(exports.routes, { useHash: true });
//# sourceMappingURL=routes.js.map