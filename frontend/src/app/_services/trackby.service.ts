import { Injectable } from '@angular/core';

import { User } from '../_models/user';

@Injectable()
export class TrackByService {

  user(index:number, user: User) {
    return user.username;
  }


}
