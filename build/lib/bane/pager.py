import requests, random, re, time, furl, sys

if sys.version_info < (3, 0):
    from urlparse import urlparse
else:
    from urllib.parse import urlparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import bs4
from bs4 import BeautifulSoup
from bane.payloads import *


def remove_html_comments(text):
    return re.sub(r"<!--(.|\s|\n)*?-->", "", text, flags=re.DOTALL)


def inputs(
    u,
    html_comments=False,
    value=False,
    timeout=10,
    user_agent=None,
    bypass=False,
    proxy=None,
    cookie=None,
):
    """
     this function is to get the names and values of input fields on a given webpage to scan.

     it takes 4 arguments:

     u: the page's link (http://...)
     value: (set by default to: False) to return the value of the fields set it to:True then the field's name and value will be string of 2
     values sperated by ":"
     timeout: (set by default to: 10) timeout flag for the request
     bypass: (set by default to: False) to bypass anti-crawlers

    usage:

    >>>import bane
    >>>link='http://www.example.com'
    >>>bane.inputs(link)
    ['email','password','rememberme']
    >>>a=bane.inputs(link,value=True)
    ['email','password','rememberme:yes','rememberme:no']

    """
    if user_agent:
        us = user_agent
    else:
        us = random.choice(ua)
    if proxy:
        proxy = {"http": "http://" + proxy, "https": "http://" + proxy}
    if bypass == True:
        u += "#"
    if cookie:
        hea = {"User-Agent": us, "Cookie": cookie}
    else:
        hea = {"User-Agent": us}
    l = []
    try:
        c = requests.get(
            u, headers=hea, proxies=proxy, timeout=timeout, verify=False
        ).text
        if html_comments == False:
            c = remove_html_comments(c)
        soup = BeautifulSoup(c, "html.parser")
        p = soup.find_all("textarea")
        for r in p:
            if r.has_attr("name"):
                s = r.get("name")
                v = r.get("value")
                if v == None:
                    v = ""
            if value == True:
                y = s + ":" + v
            else:
                y = s
            if y not in l:
                l.append(y)
        p = soup.find_all("input")
        for r in p:
            v = ""
            if r.has_attr("name"):
                s = str(r)
                s = s.split('name="')[1].split(",")[0]
                s = s.split('"')[0].split(",")[0]
                if r.has_attr("value") and (value == True):
                    v = str(r)
                    v = v.split('value="')[1].split(",")[0]
                    v = v.split('"')[0].split(",")[0]
            if value == True:
                y = s + ":" + v
            else:
                y = s
            if y not in l:
                l.append(y)
    except Exception as e:
        pass
    return l


def forms(
    u,
    value=True,
    html_comments=False,
    user_agent=None,
    timeout=10,
    bypass=False,
    proxy=None,
    cookie=None,
):
    """
    same as "inputs" function but it works on forms input fields only
    """
    if urlparse(u).path == "":
        u += "/"
    if user_agent:
        us = user_agent
    else:
        us = random.choice(ua)
    if proxy:
        proxy = {"http": "http://" + proxy, "https": "http://" + proxy}
    if bypass == True:
        u += "#"
    if cookie:
        hea = {"User-Agent": us, "Cookie": cookie}
    else:
        hea = {"User-Agent": us}
    l = []
    fom = []
    try:
        c = requests.get(
            u, headers=hea, proxies=proxy, timeout=timeout, verify=False
        ).text
        if html_comments == False:
            c = remove_html_comments(c)
        soup = BeautifulSoup(c, "html.parser")
        i = soup.find_all("form")
        for f in i:
            ac = f.get("action")
            if not ac:
                ac = u
            """if len(ac)==0:
    ac=u
   if ac[0]=="/":
    url_o="/".join(u.split('/')[:-1])
    ac=url_o+ac
   if ac[:4]!="http":
    url_o="/".join(u.split('/')[:-1])
    ac=url_o+"/"+ac"""
            if "://" not in ac:
                ur = u[: u.rfind("/")]
                if ac[0] == "/":
                    ac = ac[1 : len(ac)]
                ac = ur + "/" + ac
            me = f.get("method")
            if not me:
                me = "get"
            if len(me) == 0:
                me = "get"
            me = me.lower()
            p = f.find_all("textarea")
            for r in p:
                if r.has_attr("name"):
                    s = r.get("name")
                    v = r.get("value")
                    if v == None:
                        v = ""
                if value == True:
                    y = s + ":" + v
                else:
                    y = s
                if y not in l:
                    l.append(y)
            p = f.find_all("input")
            for r in p:
                if r.has_attr("name"):
                    s = r.get("name")
                    v = r.get("value")
                    if v == None:
                        v = ""
                if value == True:
                    y = s + ":" + v
                else:
                    y = s
                if y not in l:
                    l.append(y)
            fom.append({"inputs": l, "action": ac, "method": me})
            l = []
    except Exception as e:
        pass
    return fom


def sort_inputs(l):
    a = []
    d = []
    for x in l:
        if x["type"] not in [u"radio", u"checkbox"]:
            d.append(x)
        if x["name"] not in a and (x["type"] == u"radio" or x["type"] == u"checkbox"):
            a.append(x["name"])
    for x in a:
        d.append(
            {
                "type": [i["type"] for i in l if i["name"] == x][0],
                "name": x,
                "value": [i["value"] for i in l if i["name"] == x],
            }
        )
    return d


def forms_parser(
    u,
    html_comments=False,
    user_agent=None,
    timeout=10,
    bypass=False,
    proxy=None,
    cookie=None,
):
    """
    same as "forms" function but it return detailed information about all forms in a given page
    """
    if urlparse(u).path == "":
        u += "/"
    if user_agent:
        us = user_agent
    else:
        us = random.choice(ua)
    if proxy:
        proxy = {"http": "http://" + proxy, "https": "http://" + proxy}
    if bypass == True:
        u += "#"
    if cookie:
        hea = {"User-Agent": us, "Cookie": cookie}
    else:
        hea = {"User-Agent": us}
    l = []
    fom = []
    try:
        c = requests.get(
            u, headers=hea, proxies=proxy, timeout=timeout, verify=False
        ).text
        if html_comments == False:
            c = remove_html_comments(c)
        soup = BeautifulSoup(c, "html.parser")
        i = soup.find_all("form")
        for f in i:
            try:
                tb_inputs = f.find_all("table")[0].find_all("input")
            except:
                tb_inputs = []
            try:
                tb_textareas = f.find_all("table")[0].find_all("textarea")
            except:
                tb_textareas = []
            try:
                tb_selects = f.find_all("table")[0].find_all("select")
            except:
                tb_selects = []
            ac = f.get("action")
            enc_ty = f.get("enctype", "application/x-www-form-urlencoded")
            if not ac:
                ac = u
            """if len(ac)==0:
    ac=u
   if ac[0]=="/":
    url_o="/".join(u.split('/')[:-1])
    ac=url_o+ac
   if ac[:4]!="http":
    url_o="/".join(u.split('/')[:-1])
    ac=url_o+"/"+ac"""
            if "://" not in ac:
                ur = u[: u.rfind("/")]
                if ac[0] == "/":
                    ac = ac[1 : len(ac)]
                ac = ur + "/" + ac
            me = f.get("method", "get")
            if not me:
                me = "get"
            if len(me) == 0:
                me = "get"
            me = me.lower()
            p = f.find_all("textarea") + tb_textareas
            for r in p:
                if r.has_attr("name"):
                    s = r.get("name")
                    v = r.renderContents().decode().split("</textarea>")[0]
                    typ = r.get("type", "textarea").lower()
                    y = {"name": s, "value": v, "type": typ}
                    if y not in l:
                        l.append(y)
            h_v = {}
            p = f.find_all("input") + tb_inputs
            for r in p:
                if r.has_attr("name"):
                    s = r.get("name")
                    v = r.get("value", "")
                    typ = r.get("type", "text").lower()
                    y = {"name": s, "value": v, "type": typ}
                    if typ.lower() == "hidden":
                        h_v.update({s: v})
                    if y not in l:
                        l.append(y)
            p = f.find_all("select") + tb_selects
            opts = []
            for r in p:
                if r.has_attr("name"):
                    s = r.get("name")
                    for x in r.find_all("option"):
                        opts.append(x.text)
                    y = {"name": s, "value": opts, "type": "select"}
                    if y not in l:
                        l.append(y)
            fom.append(
                {
                    "inputs": sort_inputs(l),
                    "action": ac.lower(),
                    "enctype": enc_ty.lower(),
                    "method": me.lower(),
                    "hidden_values": h_v,
                }
            )
            l = []
    except Exception as e:
        pass
    return fom


def forms_parser_text(u, text, html_comments=False):
    """
    same as "forms" function but it return detailed information about all forms in a given page
    """
    if urlparse(u).path == "":
        u += "/"
    l = []
    fom = []
    try:
        c = text
        if html_comments == False:
            c = remove_html_comments(c)
        soup = BeautifulSoup(c, "html.parser")
        i = soup.find_all("form")
        for f in i:
            try:
                tb_inputs = f.find_all("table")[0].find_all("input")
            except:
                tb_inputs = []
            try:
                tb_textareas = f.find_all("table")[0].find_all("textarea")
            except:
                tb_textareas = []
            try:
                tb_selects = f.find_all("table")[0].find_all("select")
            except:
                tb_selects = []
            ac = f.get("action")
            enc_ty = f.get("enctype", "application/x-www-form-urlencoded").lower()
            if not ac:
                ac = u
            """if len(ac)==0:
    ac=u
   if ac[0]=="/":
    url_o="/".join(u.split('/')[:-1])
    ac=url_o+ac
   if ac[:4]!="http":
    url_o="/".join(u.split('/')[:-1])
    ac=url_o+"/"+ac"""
            if "://" not in ac:
                ur = u[: u.rfind("/")]
                if ac[0] == "/":
                    ac = ac[1 : len(ac)]
                ac = ur + "/" + ac
            me = f.get("method", "get").lower()
            if not me:
                me = "get"
            if len(me) == 0:
                me = "get"
            me = me.lower()
            p = f.find_all("textarea") + tb_textareas
            for r in p:
                if r.has_attr("name"):
                    s = r.get("name")
                    v = r.renderContents().decode().split("</textarea>")[0]
                    typ = r.get("type", "textarea").lower()
                    y = {"name": s, "value": v, "type": typ}
                    if y not in l:
                        l.append(y)
            h_v = {}
            p = f.find_all("input") + tb_inputs
            for r in p:
                if r.has_attr("name"):
                    s = r.get("name")
                    v = r.get("value", "")
                    typ = r.get("type", "text").lower()
                    y = {"name": s, "value": v, "type": typ}
                    if typ.lower() == "hidden":
                        h_v.update({s: v})
                    if y not in l:
                        l.append(y)
            p = f.find_all("select") + tb_selects
            opts = []
            for r in p:
                if r.has_attr("name"):
                    s = r.get("name")
                    for x in r.find_all("option"):
                        opts.append(x.text)
                    y = {"name": s, "value": opts, "type": "select"}
                    if y not in l:
                        l.append(y)
            fom.append(
                {
                    "inputs": sort_inputs(l),
                    "action": ac,
                    "enctype": enc_ty,
                    "method": me,
                    "hidden_values": h_v,
                }
            )
            l = []
    except Exception as e:
        pass
    return fom


def cookies_to_dict(cookies):
    d = {}
    a = cookies.split(";")
    for x in a:
        if "=" in x:
            d.update({x.split("=")[0].strip(): x.split("=")[1].strip()})
    return d


def update_cookies(cookies, cook):
    c1 = {}
    c2 = {}
    if cookies:
        c1 = cookies_to_dict(cookies)
    if cook:
        c2 = cookies_to_dict(cook)
    c2.update(c1)
    cookie = ""
    for x in c2:
        cookie += x + "=" + c2[x] + ";"
    return cookie


def set_correct_cookies(new_cookies, cookie=None):
    if not cookie:
        cookie = ""
    if not new_cookies:
        new_cookies = ""
    if cookie and len(cookie) > 0:
        if new_cookies and len(new_cookies) > 0:
            cookies = update_cookies(new_cookies, cookie)
        else:
            cookies = cookie
    else:
        cookies = new_cookies
    return cookies


def set_up_injection(
    url,
    form_index,
    parameter,
    payload,
    cookie,
    user_agent,
    proxy,
    timeout,
    auto_fill,
    file_extension="png",
    dont_change={},
    number=(1, 9),
    leave_empty=[],
    dont_send=[],
    mime_type=None,
    predefined_inputs={},
):
    cookies = None
    if proxy:
        proxy = {"http": "http://" + proxy, "https": "http://" + proxy}
    h = {"User-Agent": user_agent}
    if cookie:
        h.update({"Cookie": cookie})
        cookies = cookie
    try:
        r = requests.get(url, proxies=proxy, headers=h, verify=False, timeout=timeout)
    except:
        return False
    cook = None
    try:
        cook = r.headers["Set-cookie"]
    except:
        pass
    cookies = set_correct_cookies(cook, cookie=cookie)
    form = forms_parser_text(url, r.text)[form_index]
    h = {"User-Agent": user_agent}
    if cookies and len(cookies.strip()) > 0:
        h.update({"Cookie": cookies})
    return (
        form_filler(
            form,
            parameter,
            payload,
            auto_fill=auto_fill,
            number=number,
            dont_change=dont_change,
            file_extension=file_extension,
            leave_empty=leave_empty,
            dont_send=dont_send,
            mime_type=mime_type,
            predefined_inputs=predefined_inputs,
        ),
        h,
        proxy,
        timeout,
    )


def form_filler(
    form,
    param,
    payload,
    file_extension="png",
    dont_change={},
    number=(1, 9),
    auto_fill=10,
    leave_empty=[],
    dont_send=[],
    mime_type=None,
    predefined_inputs={},
):
    for x in form["inputs"]:
        if x["name"].strip() in dont_change:
            x["value"] = dont_change[x["name"]]
        else:
            if x["name"].strip() in dont_send:
                form["inputs"].remove(x)
            else:
                if x["name"].strip() not in leave_empty:
                    if x["name"].strip() == param:
                        if x["type"] == "file":
                            if not mime_type:
                                x["value"] = (
                                    payload + "." + file_extension,
                                    files_upload[file_extension],
                                )
                            else:
                                x["value"] = (
                                    payload + "." + file_extension,
                                    files_upload[file_extension],
                                    mime_type,
                                )
                        else:
                            x["value"] = payload
                    else:
                        if x["name"].strip() in predefined_inputs:
                            x["value"] = predefined_inputs[x["name"]]
                        else:
                            if x["value"] == "":
                                if x["type"] == "file":
                                    if not mime_type:
                                        x["value"] = (
                                            "bane_test"
                                            + str(random.randint(100000, 999999))
                                            + "."
                                            + file_extension,
                                            files_upload[file_extension],
                                        )
                                    else:
                                        x["value"] = (
                                            "bane_test"
                                            + str(random.randint(100000, 999999))
                                            + "."
                                            + file_extension,
                                            files_upload[file_extension],
                                            mime_type,
                                        )
                                else:
                                    if x["type"] == "number":
                                        for i in range(number[0], number[1]):
                                            x["value"] += str(random.randint(1, 9))
                                    else:
                                        for i in range(auto_fill):
                                            x["value"] += random.choice(lis)
                            if x["type"] in ["select", "radio", "checkbox"]:
                                if len(x["value"]) == 0 or x["value"] == "":
                                    x["value"] = ""
                                    for i in range(auto_fill):
                                        x["value"] += random.choice(lis)
                                else:
                                    x["value"] = random.choice(x["value"])
    return form


def get_login_form(url, text):
    a = forms_parser_text(url, text)
    for x in a:
        for i in x["inputs"]:
            if i["type"].lower().strip() == "password":
                return x
    raise Exception("No login form")


def set_login_form(url, text, username, password):
    a = get_login_form(url, text)
    d = {}
    for x in a["inputs"]:
        if x["type"].lower().strip() == "password":
            d.update({x["name"]: password})
        elif (
            x["type"].lower().strip() == "text"
            or x["type"].lower().strip() == "email"
            or x["type"].lower().strip() == "tel"
        ):
            d.update({x["name"]: username})
        else:
            d.update({x["name"]: x["value"]})
    return [d, a["action"]]


def get_upload_form(a):
    for x in a:
        for i in x["inputs"]:
            if i["type"].lower().strip() == "file":
                return x
    raise Exception("No file upload form")


def get_upload_form_text(url, text):
    a = forms_parser_text(url, text)
    for x in a:
        for i in x["inputs"]:
            if i["type"].lower().strip() == "file":
                return x
    raise Exception("No file upload form")


def crawl(
    u,
    timeout=10,
    html_comments=False,
    user_agent=None,
    bypass=False,
    proxy=None,
    cookie=None,
):
    """
    this function is used to crawl any given link and returns a list of all available links on that webpage with ability to bypass anti-crawlers

    the function takes those arguments:

    u: the targeted link
    timeout: (set by default to 10) timeout flag for the request
    bypass: (set by default to False) option to bypass anti-crawlers by simply adding "#" to the end of the link :)

    usage:

    >>>import bane
    >>>url='http://www.example.com'
    >>>bane.crawl(url)

    >>>bane.crawl(url,bypass=True)"""
    if urlparse(u).path == "":
        u += "/"
    if u.split("?")[0][-1] != "/" and "." not in u.split("?")[0].rsplit("/", 1)[-1]:
        u = u.replace("?", "/?")
    if user_agent:
        us = user_agent
    else:
        us = random.choice(ua)
    if proxy:
        proxy = {"http": "http://" + proxy, "https": "http://" + proxy}
    h = {}
    if bypass == True:
        u += "#"
    if cookie:
        hea = {"User-Agent": us, "Cookie": cookie}
    else:
        hea = {"User-Agent": us}
    try:
        c = requests.get(
            u, headers=hea, proxies=proxy, timeout=timeout, verify=False
        ).text
        if html_comments == False:
            c = remove_html_comments(c)
        soup = BeautifulSoup(c, "html.parser")
        ur = u.replace(u.split("/")[-1], "")
        """if ur[-1]=='/':
   ur=ur[:-1]"""
        index_link = 0
        h.update(
            {
                -1: (
                    "Source_url",
                    u,
                    urlparse(u).path,
                    [(x, furl.furl(u).args[x]) for x in furl.furl(u).args],
                )
            }
        )
        for a in soup.find_all("a"):
            u = ur
            if a.has_attr("href"):
                try:
                    txt = a.text
                    a = str(a["href"])
                    if "://" not in a:
                        if a[0] == "/":
                            a = a[1 : len(a)]
                        a = u + a
                    if (a not in h.values()) and (u in a):
                        if (a != u + "/") and (a != u):
                            h.update(
                                {
                                    index_link: (
                                        txt,
                                        a,
                                        urlparse(a).path,
                                        [
                                            (x, furl.furl(a).args[x])
                                            for x in furl.furl(a).args
                                        ],
                                    )
                                }
                            )
                            index_link += 1
                except Exception as e:
                    pass
    except Exception as ex:
        pass
    return h


def crawl_text(u, text, html_comments=False):
    """
    this function is used to crawl any given link and returns a list of all available links on that webpage with ability to bypass anti-crawlers

    the function takes those arguments:

    u: the targeted link
    timeout: (set by default to 10) timeout flag for the request
    bypass: (set by default to False) option to bypass anti-crawlers by simply adding "#" to the end of the link :)

    usage:

    >>>import bane
    >>>url='http://www.example.com'
    >>>bane.crawl(url)

    >>>bane.crawl(url,bypass=True)"""
    if urlparse(u).path == "":
        u += "/"
    if u.split("?")[0][-1] != "/" and "." not in u.split("?")[0].rsplit("/", 1)[-1]:
        u = u.replace("?", "/?")
    try:
        c = text
        if html_comments == False:
            c = remove_html_comments(c)
        soup = BeautifulSoup(c, "html.parser")
        ur = u.replace(u.split("/")[-1], "")
        """if ur[-1]=='/':
   ur=ur[:-1]"""
        index_link = 0
        h.update(
            {
                -1: (
                    "Source_url",
                    u,
                    urlparse(u).path,
                    [(x, furl.furl(u).args[x]) for x in furl.furl(u).args],
                )
            }
        )
        for a in soup.find_all("a"):
            u = ur
            if a.has_attr("href"):
                try:
                    txt = a.text
                    a = str(a["href"])
                    if "://" not in a:
                        if a[0] == "/":
                            a = a[1 : len(a)]
                        a = u + a
                    if (a not in h.values()) and (u in a):
                        if (a != u + "/") and (a != u):
                            h.update(
                                {
                                    index_link: (
                                        txt,
                                        a,
                                        urlparse(a).path,
                                        [
                                            (x, furl.furl(a).args[x])
                                            for x in furl.furl(a).args
                                        ],
                                    )
                                }
                            )
                            index_link += 1
                except Exception as e:
                    pass
    except Exception as ex:
        pass
    return h


def media(
    u,
    timeout=10,
    html_comments=False,
    user_agent=None,
    bypass=False,
    proxy=None,
    cookie=None,
):
    """
    this funtion was made to collect the social media links related to the targeted link (facebook, twitter, instagram...).

    the function takes those arguments:

    u: the targeted link
    timeout: (set by default to 10) timeout flag for the request
    bypass: (set by default to False) option to bypass anti-crawlers by simply adding "#" to the end of the link :)

    usage:

    >>>import bane
    >>>url='http://www.example.com'
    >>>bane.media(url)

    >>>bane.media(url,bypass=True)"""
    if urlparse(u).path == "":
        u += "/"
    if user_agent:
        us = user_agent
    else:
        us = random.choice(ua)
    if cookie:
        hea = {"User-Agent": us, "Cookie": cookie}
    else:
        hea = {"User-Agent": us}
    h = {}
    if proxy:
        proxy = {"http": "http://" + proxy, "https": "http://" + proxy}
    try:
        if bypass == True:
            u += "#"
        if cookie:
            hea = {"User-Agent": us, "Cookie": cookie}
        else:
            hea = {"User-Agent": us}
        c = requests.get(
            u, headers=hea, proxies=proxy, timeout=timeout, verify=False
        ).text
        if html_comments == False:
            c = remove_html_comments(c)
        soup = BeautifulSoup(c, "html.parser")
        ul = u.split("://")[1].split('"')[0]
        ur = ul.replace("www.", "")
        for a in soup.findAll("a"):
            try:
                if (
                    a.has_attr("href")
                    and (u not in a["href"])
                    and (ur not in a["href"])
                    and (a["href"][:4] == "http")
                ):
                    txt = a.text
                    if a["href"] not in h:
                        h.update({txt: a["href"]})
            except:
                pass
    except:
        pass
    return h


def subdomains_extract(
    u,
    timeout=10,
    html_comments=False,
    user_agent=None,
    bypass=False,
    proxy=None,
    cookie=None,
):
    """
    this function collects the subdomains found on the targeted webpage.

    the function takes those arguments:

    u: the targeted link
    timeout: (set by default to 10) timeout flag for the request
    bypass: (set by default to False) option to bypass anti-crawlers by simply adding "#" to the end of the link :)

    usage:

    >>>import bane
    >>>url='http://www.example.com'
    >>>bane.subdomains_extract(url)

    >>>bane.subdomains_extract(url,bypass=True)"""
    if urlparse(u).path == "":
        u += "/"
    if user_agent:
        us = user_agent
    else:
        us = random.choice(ua)
    if proxy:
        proxy = {"http": "http://" + proxy, "https": "http://" + proxy}
    h = {}
    if cookie:
        hea = {"User-Agent": us, "Cookie": cookie}
    else:
        hea = {"User-Agent": us}
    try:
        if bypass == True:
            u += "#"
        c = requests.get(
            u, headers=hea, proxies=proxy, timeout=timeout, verify=False
        ).text
        if html_comments == False:
            c = remove_html_comments(c)
        ul = u.split("://")[1].split("/")[0]
        soup = BeautifulSoup(c, "html.parser")
        for a in soup.findAll("a"):
            if (
                a.has_attr("href")
                and (ul.replace("www", "") in a["href"])
                and (ul not in a["href"])
                and (a["href"][:4] == "http")
            ):
                txt = a.text
                try:
                    hr = a["href"].split("://")[1].split("/")[0]
                    h.update({txt: hr})
                except Exception as e:
                    pass
    except Exception as e:
        pass
    return h
