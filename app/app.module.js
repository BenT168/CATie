"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var platform_browser_1 = require('@angular/platform-browser');
var ng_semantic_1 = require("ng-semantic");
var app_component_1 = require('./components/app.component');
var routes_1 = require("./routes");
var home_component_1 = require('./components/home/home.component');
var reviews_component_1 = require('./components/reviews/reviews.component');
var add_component_1 = require("./components/reviews/add/add.component");
var statistic_component_1 = require("./components/reviews/statistic/statistic.component");
var events_component_1 = require("./components/events/events.component");
var auth_1 = require("./services/auth");
var AppModule = (function () {
    function AppModule() {
    }
    AppModule = __decorate([
        core_1.NgModule({
            imports: [
                platform_browser_1.BrowserModule,
                ng_semantic_1.NgSemanticModule,
                routes_1.routing
            ],
            providers: [
                routes_1.APP_ROUTER_PROVIDERS,
                auth_1.Auth
            ],
            declarations: [
                app_component_1.AppComponent,
                home_component_1.HomeComponent,
                reviews_component_1.ReviewComponent,
                add_component_1.AddReviewComponent,
                statistic_component_1.StatisticReviewComponent,
                events_component_1.EventsComponent
            ],
            bootstrap: [
                app_component_1.AppComponent
            ]
        }), 
        __metadata('design:paramtypes', [])
    ], AppModule);
    return AppModule;
}());
exports.AppModule = AppModule;
//# sourceMappingURL=app.module.js.map