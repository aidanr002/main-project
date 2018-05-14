CREATE TABLE pending_comments (
  pendingcommentid INTEGER PRIMARY KEY NOT NULL,
  topicid INTEGER NOT NULL,
  username TEXT NOT NULL,
  usercountry TEXT NOT NULL,
  stance TEXT NOT NULL,
  comment TEXT NOT NULL
);
