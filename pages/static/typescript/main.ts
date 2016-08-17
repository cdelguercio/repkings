import {bootstrap} from '@angular/platform-browser-dynamic';
import {provide, enableProdMode} from '@angular/core';
import {ROUTER_PROVIDERS} from '@angular/router-deprecated';
import {APP_BASE_HREF} from '@angular/common';
import {DashboardComponent} from './dashboard.component';

import { disableDeprecatedForms, provideForms } from '@angular/forms';

declare var window: any;

if( window.PRODUCTION == 'True' ) {
    enableProdMode();
}

bootstrap(DashboardComponent, [ROUTER_PROVIDERS, {provide: APP_BASE_HREF, useValue: '/'}, disableDeprecatedForms(), provideForms()]);
