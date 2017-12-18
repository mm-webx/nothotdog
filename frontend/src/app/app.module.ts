import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';


import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MaterialModule} from "./material.config";
import {RouterModule, Routes} from "@angular/router";
import {NotFoundComponent} from './not-found/not-found.component';
import {HotDogDetailsComponent} from './hot-dog-details/hot-dog-details.component';
import {HotDogListComponent} from './hot-dog-list/hot-dog-list.component';
import {HotDogHomeComponent} from './hot-dog-home/hot-dog-home.component';
import {CookieModule} from "ngx-cookie";
import {HttpClientModule} from '@angular/common/http';
import {ApiService} from "./api.service";
import {LoginComponent} from './login/login.component';
import {RegisterComponent} from './register/register.component';
import {BaseComponent} from './base/base.component';
import {FormsModule} from "@angular/forms";
import {SocketService} from "./socket.service";
import {WebSocketService} from "angular2-websocket-service";
import {HotDogResultComponent} from './hot-dog-result/hot-dog-result.component';

const appRoutes: Routes = [
  {path: 'home', component: HotDogHomeComponent},
  {path: 'login', component: LoginComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'result', component: HotDogResultComponent},
  {path: 'hotdog', component: HotDogDetailsComponent},
  {
    path: 'hotdogs',
    component: HotDogListComponent,
  },
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {path: '**', component: NotFoundComponent}
];

@NgModule({
  declarations: [
    AppComponent,
    NotFoundComponent,
    HotDogDetailsComponent,
    HotDogListComponent,
    HotDogHomeComponent,
    LoginComponent,
    RegisterComponent,
    BaseComponent,
    HotDogResultComponent
  ],
  imports: [
    RouterModule.forRoot(
      appRoutes
    ),
    BrowserModule,
    HttpClientModule,
    MaterialModule,
    BrowserAnimationsModule,
    CookieModule.forRoot(),
    FormsModule
  ],
  providers: [
    ApiService,
    SocketService,
    WebSocketService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
