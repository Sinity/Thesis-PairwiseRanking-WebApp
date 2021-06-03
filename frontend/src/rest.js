export const REST = {
  login, logout, userIdentity,
  refreshToken,
  post, get, put, del
};

const baseURL = 'http://localhost:5000';
const storageAuth = 'auth';

function userIdentity() {
  return JSON.parse(localStorage.getItem(storageAuth));
}

function logout() {
  localStorage.removeItem(storageAuth);
}

async function get(endpoint) {
  return backendReq('GET', endpoint);
}

async function post(endpoint, body = {}) {
  return backendReq('POST', endpoint, body);
}

async function put(endpoint, body = {}) {
  return backendReq('PUT', endpoint, body);
}

async function del(endpoint, body = {}) {
  return backendReq('DELETE', endpoint, body);
}

async function login(email, password) {
  logout();
  console.log('Login attempt...')
  const requestParams = {
    method: 'POST',
    headers: requestHeaders(),
    body: JSON.stringify({'email': email, 'password': password})
  };
  const resp = await fetch(baseURL + '/auth', requestParams);
  const respBody = await resp.json();

  if (!resp.ok) {
    console.log('Login attempt failed, status=', resp.status, 'body=', respBody)
    return respBody['message'];
  }

  let authData = {
    accessToken: respBody.access_token,
    refreshToken: respBody.refresh_token,
    identity: respBody.identity
  };
  localStorage.setItem(storageAuth, JSON.stringify(authData));
  console.log('Logged in', authData)
  return '';
}


async function refreshToken() {
  console.log('Refreshing access token...')
  let uid = userIdentity();
  if (uid === null) {
    console.log('Cant refresh access token; user not logged in')
    return false;
  }

  const requestParams = {
    method: 'GET',
    headers: requestHeaders(uid.refreshToken),
  };
  const resp = await fetch(baseURL + '/auth', requestParams);
  const respBody = await resp.json();

  let refreshedToken = respBody.access_token;
  if (!refreshedToken) {
    console.log('Didnt receive refreshed token.');
    localStorage.setItem(storageAuth, null);
    return false;
  }

  console.log('Received refreshed token', refreshedToken);
  uid.accessToken = refreshedToken;
  localStorage.setItem(storageAuth, JSON.stringify(uid));
  return true;
}

async function backendReq(method, endpoint, body = {}) {
  let authToken = '';
  if (userIdentity() !== null)
    authToken = userIdentity().accessToken;

  let requestParams = {};
  requestParams['method'] = method;
  requestParams['headers'] = requestHeaders(authToken);
  if (method !== 'GET')
    requestParams['body'] = JSON.stringify(body);
  console.log('Request to the backend', method, endpoint, requestParams)
  let resp = await fetch(baseURL + endpoint, requestParams);

  if (!resp.ok) {
    console.log('HTTP status error', resp.status);
    if ((resp.status === 401) && userIdentity() !== null) {
      let auth = userIdentity()
      auth.accessToken = '';
      localStorage.setItem(storageAuth, JSON.stringify(auth));
      console.log('Attempting to refresh access token');
      await refreshToken();
      console.log('Token value after refresh', userIdentity().accessToken);
      console.log('Attempt sending request again...');
      if (userIdentity().accessToken)
        return backendReq(method, endpoint, body);
      console.log('Failed, logging out.');
      localStorage.setItem(storageAuth, null);
    }
  }

  return resp;
}

function requestHeaders(jwtToken = '') {
  let headers = { 'Content-Type': 'application/json' };
  if (jwtToken != '')
    headers.Authorization = 'Bearer ' + jwtToken;
  return headers;
}

