import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';


import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MaterialModule} from "./material.config";
import {RouterModule, Routes} from "@angular/router";
import {NotFoundComponent} from './not-found/not-found.component';
import {HotDogAddComponent} from './hot-dog-add/hot-dog-add.component';
import {HotDogDetailsComponent} from './hot-dog-details/hot-dog-details.component';
import {HotDogListComponent} from './hot-dog-list/hot-dog-list.component';
import {HotDogHomeComponent} from './hot-dog-home/hot-dog-home.component';
import {HotDogAboutComponent} from './hot-dog-about/hot-dog-about.component';

const appRoutes: Routes = [
  {path: 'home', component: HotDogHomeComponent},
  {path: 'about', component: HotDogAboutComponent},
  {path: 'add', component: HotDogAddComponent},
  {path: 'hotdog/:id', component: HotDogDetailsComponent},
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
    HotDogAddComponent,
    HotDogDetailsComponent,
    HotDogListComponent,
    HotDogHomeComponent,
    HotDogAboutComponent
  ],
  imports: [
    RouterModule.forRoot(
      appRoutes,
      {enableTracing: true} // debug only
    ),
    BrowserModule,
    MaterialModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
