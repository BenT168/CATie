import {
    Component, ChangeDetectionStrategy, ViewChild, TemplateRef,
    Input
} from '@angular/core';
import {
    startOfDay,
    endOfDay,
    subDays,
    addDays,
    endOfMonth,
    isSameDay,
    isSameMonth,
    addHours
} from 'date-fns';
import { Subject } from 'rxjs/Subject';
import {
    CalendarEvent,
    CalendarEventAction,
    CalendarEventTimesChangedEvent,
    CalendarUtils
} from 'angular-calendar';
import {WeekDay} from "calendar-utils/dist/calendarUtils";

const colors: any = {
    red: {
        primary: '#ad2121',
        secondary: '#FAE3E3'
    },
    blue: {
        primary: '#1e90ff',
        secondary: '#D1E8FF'
    },
    yellow: {
        primary: '#e3bc08',
        secondary: '#FDF1BA'
    }
};

@Component({
  selector: 'app-calendar',
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss']
})
export class CalendarComponent {

  @ViewChild('modalContent') modalContent: TemplateRef<any>;

    @Input() locale: string = 'en';

    view: string = 'month';

    viewDate: Date = new Date();

    dayStart: number = 9;
    dayEnd: number = 18;

    /*actions: CalendarEventAction[] = [{
        label: '<i class="fa fa-fw fa-pencil"></i>',
        onClick: ({event}: {event: CalendarEvent}): void => {
            this.handleEvent('Edited', event);
        }
    }, {
        label: '<i class="fa fa-fw fa-times"></i>',
        onClick: ({event}: {event: CalendarEvent}): void => {
            this.events = this.events.filter(iEvent => iEvent !== event);
            this.handleEvent('Deleted', event);
        }
    }];*/

    refresh: Subject<any> = new Subject();

    days: WeekDay[];

    monEvents: CalendarEvent[] = [{
        start: subDays(startOfDay(new Date()), 1),
        end: addDays(new Date(), 1),
        title: 'A 3 day event',
        color: colors.red,
        //actions: this.actions
    }, {
        start: startOfDay(new Date()),
        title: 'An event with no end date',
        color: colors.yellow,
        //actions: this.actions
    }, {
        start: subDays(endOfMonth(new Date()), 3),
        end: addDays(endOfMonth(new Date()), 3),
        title: 'A long event that spans 2 months',
        color: colors.blue
    }, {
        start: addHours(startOfDay(new Date()), 2),
        end: new Date(),
        title: 'A draggable and resizable event',
        color: colors.yellow,
        //actions: this.actions,
        resizable: {
            beforeStart: true,
            afterEnd: true
        },
        draggable: true
    }];

    tueEvents: CalendarEvent[] = [{
        start: subDays(startOfDay(new Date()), 1),
        end: addDays(new Date(), 1),
        title: 'A 3 day event',
        color: colors.red,
        //actions: this.actions
    }, {
        start: startOfDay(new Date()),
        title: 'An event with no end date',
        color: colors.yellow,
        //actions: this.actions
    }, {
        start: subDays(endOfMonth(new Date()), 3),
        end: addDays(endOfMonth(new Date()), 3),
        title: 'A long event that spans 2 months',
        color: colors.blue
    }, {
        start: addHours(startOfDay(new Date()), 2),
        end: new Date(),
        title: 'A draggable and resizable event',
        color: colors.yellow,
        //actions: this.actions,
        resizable: {
            beforeStart: true,
            afterEnd: true
        },
        draggable: true
    }];

    wedEvents: CalendarEvent[] = [{
        start: subDays(startOfDay(new Date()), 1),
        end: addDays(new Date(), 1),
        title: 'A 3 day event',
        color: colors.red,
        //actions: this.actions
    }, {
        start: startOfDay(new Date()),
        title: 'An event with no end date',
        color: colors.yellow,
        //actions: this.actions
    }, {
        start: subDays(endOfMonth(new Date()), 3),
        end: addDays(endOfMonth(new Date()), 3),
        title: 'A long event that spans 2 months',
        color: colors.blue
    }, {
        start: addHours(startOfDay(new Date()), 2),
        end: new Date(),
        title: 'A draggable and resizable event',
        color: colors.yellow,
        //actions: this.actions,
        resizable: {
            beforeStart: true,
            afterEnd: true
        },
        draggable: true
    }];

    thuEvents: CalendarEvent[] = [{
        start: subDays(startOfDay(new Date()), 1),
        end: addDays(new Date(), 1),
        title: 'A 3 day event',
        color: colors.red,
        //actions: this.actions
    }, {
        start: startOfDay(new Date()),
        title: 'An event with no end date',
        color: colors.yellow,
        //actions: this.actions
    }, {
        start: subDays(endOfMonth(new Date()), 3),
        end: addDays(endOfMonth(new Date()), 3),
        title: 'A long event that spans 2 months',
        color: colors.blue
    }, {
        start: addHours(startOfDay(new Date()), 2),
        end: new Date(),
        title: 'A draggable and resizable event',
        color: colors.yellow,
        //actions: this.actions,
        resizable: {
            beforeStart: true,
            afterEnd: true
        },
        draggable: true
    }];

    friEvents: CalendarEvent[] = [{
        start: subDays(startOfDay(new Date()), 1),
        end: addDays(new Date(), 1),
        title: 'A 3 day event',
        color: colors.red,
        //actions: this.actions
    }, {
        start: startOfDay(new Date()),
        title: 'An event with no end date',
        color: colors.yellow,
        //actions: this.actions
    }, {
        start: subDays(endOfMonth(new Date()), 3),
        end: addDays(endOfMonth(new Date()), 3),
        title: 'A long event that spans 2 months',
        color: colors.blue
    }, {
        start: addHours(startOfDay(new Date()), 2),
        end: new Date(),
        title: 'A draggable and resizable event',
        color: colors.yellow,
        //actions: this.actions,
        resizable: {
            beforeStart: true,
            afterEnd: true
        },
        draggable: true
    }];

    satEvents: CalendarEvent[] = [{
        start: subDays(startOfDay(new Date()), 1),
        end: addDays(new Date(), 1),
        title: 'A 3 day event',
        color: colors.red,
        //actions: this.actions
    }, {
        start: startOfDay(new Date()),
        title: 'An event with no end date',
        color: colors.yellow,
        // actions: this.actions
    }, {
        start: subDays(endOfMonth(new Date()), 3),
        end: addDays(endOfMonth(new Date()), 3),
        title: 'A long event that spans 2 months',
        color: colors.blue
    }, {
        start: addHours(startOfDay(new Date()), 2),
        end: new Date(),
        title: 'A draggable and resizable event',
        color: colors.yellow,
        //actions: this.actions,
        resizable: {
            beforeStart: true,
            afterEnd: true
        },
        draggable: true
    }];

    sunEvents: CalendarEvent[] = [{
        start: subDays(startOfDay(new Date()), 1),
        end: addDays(new Date(), 1),
        title: 'A 3 day event',
        color: colors.red,
        //actions: this.actions
    }, {
        start: startOfDay(new Date()),
        title: 'An event with no end date',
        color: colors.yellow,
        //actions: this.actions
    }, {
        start: subDays(endOfMonth(new Date()), 3),
        end: addDays(endOfMonth(new Date()), 3),
        title: 'A long event that spans 2 months',
        color: colors.blue
    }, {
        start: addHours(startOfDay(new Date()), 2),
        end: new Date(),
        title: 'A draggable and resizable event',
        color: colors.yellow,
        // actions: this.actions,
        resizable: {
            beforeStart: true,
            afterEnd: true
        },
        draggable: true
    }];

    activeDayIsOpen: boolean = true;

    constructor(private utils: CalendarUtils) {}

    ngOnChanges(changes: any): void {

        if (changes.viewDate) {
            this.refreshHeader();
        }
    }

    dayClicked({date, events}: {date: Date, events: CalendarEvent[]}): void {

        if (isSameMonth(date, this.viewDate)) {
            if (
                (isSameDay(this.viewDate, date) && this.activeDayIsOpen === true) ||
                events.length === 0
            ) {
                this.activeDayIsOpen = false;
            } else {
                this.activeDayIsOpen = true;
                this.viewDate = date;
            }
        }
    }

    eventTimesChanged({event, newStart, newEnd}: CalendarEventTimesChangedEvent): void {
        event.start = newStart;
        event.end = newEnd;
        this.handleEvent('Dropped or resized', event);
        this.refresh.next();
    }

    handleEvent(action: string, event: CalendarEvent): void {

    }

    private refreshHeader(): void {
        this.days = this.utils.getWeekViewHeader({
            viewDate: this.viewDate,
            weekStartsOn: 0
        });
    }

    private refreshAll(): void {
        this.refreshHeader();
    }

    // addEvent(): void {
    //     this.events.push({
    //         title: 'New event',
    //         start: startOfDay(new Date()),
    //         end: endOfDay(new Date()),
    //         color: colors.red,
    //         draggable: true,
    //         resizable: {
    //             beforeStart: true,
    //             afterEnd: true
    //         }
    //     });
    //     this.refresh.next();
    // }

}

/*

const colors: any = {
    red: {
        primary: '#ad2121',
        secondary: '#FAE3E3'
    },
    blue: {
        primary: '#1e90ff',
        secondary: '#D1E8FF'
    },
    yellow: {
        primary: '#e3bc08',
        secondary: '#FDF1BA'
    }
};

export class DemoComponent {

    @ViewChild('modalContent') modalContent: TemplateRef<any>;

    view: string = 'month';

    viewDate: Date = new Date();

    modalData: {
        action: string,
        event: CalendarEvent
    };

    actions: CalendarEventAction[] = [{
        label: '<i class="fa fa-fw fa-pencil"></i>',
        onClick: ({event}: {event: CalendarEvent}): void => {
            this.handleEvent('Edited', event);
        }
    }, {
        label: '<i class="fa fa-fw fa-times"></i>',
        onClick: ({event}: {event: CalendarEvent}): void => {
            this.events = this.events.filter(iEvent => iEvent !== event);
            this.handleEvent('Deleted', event);
        }
    }];

    refresh: Subject<any> = new Subject();

    events: CalendarEvent[] = [{
        start: subDays(startOfDay(new Date()), 1),
        end: addDays(new Date(), 1),
        title: 'A 3 day event',
        color: colors.red,
        actions: this.actions
    }, {
        start: startOfDay(new Date()),
        title: 'An event with no end date',
        color: colors.yellow,
        actions: this.actions
    }, {
        start: subDays(endOfMonth(new Date()), 3),
        end: addDays(endOfMonth(new Date()), 3),
        title: 'A long event that spans 2 months',
        color: colors.blue
    }, {
        start: addHours(startOfDay(new Date()), 2),
        end: new Date(),
        title: 'A draggable and resizable event',
        color: colors.yellow,
        actions: this.actions,
        resizable: {
            beforeStart: true,
            afterEnd: true
        },
        draggable: true
    }];

    activeDayIsOpen: boolean = true;

    constructor(private modal: NgbModal) {}

    dayClicked({date, events}: {date: Date, events: CalendarEvent[]}): void {

        if (isSameMonth(date, this.viewDate)) {
            if (
                (isSameDay(this.viewDate, date) && this.activeDayIsOpen === true) ||
                events.length === 0
            ) {
                this.activeDayIsOpen = false;
            } else {
                this.activeDayIsOpen = true;
                this.viewDate = date;
            }
        }
    }

    eventTimesChanged({event, newStart, newEnd}: CalendarEventTimesChangedEvent): void {
        event.start = newStart;
        event.end = newEnd;
        this.handleEvent('Dropped or resized', event);
        this.refresh.next();
    }

    handleEvent(action: string, event: CalendarEvent): void {
        this.modalData = {event, action};
        this.modal.open(this.modalContent, {size: 'lg'});
    }

    addEvent(): void {
        this.events.push({
            title: 'New event',
            start: startOfDay(new Date()),
            end: endOfDay(new Date()),
            color: colors.red,
            draggable: true,
            resizable: {
                beforeStart: true,
                afterEnd: true
            }
        });
        this.refresh.next();
    }

} */
